# One bibliography powers public landing pages, scholarly metadata, and exports.
# Keep citation downloads as BibTeX objects until serialization: deleting lines
# can leave behind continuation lines from multiline website-only fields.
require 'bibtex'
require 'json'
require 'fileutils'

module Jekyll
  # Jekyll Scholar has a .bib converter that turns a Page into formatted HTML,
  # even without a layout. Static files bypass converters and Liquid entirely.
  class PublicationExport < StaticFile
    def initialize(site, path, content)
      super(site, site.source, File.dirname(path), File.basename(path))
      @content = content
      @data = { 'sitemap' => false, 'search' => false }
    end

    def modified_time
      @site.time
    end

    def modified?
      true
    end

    def write(destination_directory)
      output_path = destination(destination_directory)
      FileUtils.mkdir_p(File.dirname(output_path))
      File.binwrite(output_path, @content)
      true
    end
  end

  class PaperPagesGenerator < Generator
    safe true
    priority :low

    MONTHS = %w[jan feb mar apr may jun jul aug sep oct nov dec].freeze
    WEBSITE_FIELDS = %w[abbr abstract additional_info altmetric arxiv award award_name bibtex_show blog code html
                        pdf poster preview selected slides supp video website month_numeric].freeze

    def generate(site)
      scholar = site.config['scholar'] || {}
      bib_path = File.join(site.source, scholar['source'] || '_bibliography', scholar['bibliography'] || 'papers.bib')
      return unless File.exist?(bib_path)

      source = File.read(bib_path).sub(/\A---\s*\n.*?\n---\s*\n/m, '')
      raw_bibliography = BibTeX.parse(source)
      raise "Invalid bibliography: #{bib_path}" if raw_bibliography.errors?

      # Resolve @string references so each downloadable entry is self-contained.
      raw_bibliography.replace_strings.join_strings
      bibliography = raw_bibliography.dup.convert(:latex)
      filtered = (WEBSITE_FIELDS + Array(site.config['filtered_bibtex_keywords'])).uniq
      papers = bibliography.each_entry.map do |entry|
        paper_data(site, entry, raw_bibliography[entry.key], filtered)
      end.sort_by { |paper| [-paper['year'].to_i, -paper['month_number'].to_i, paper['key']] }
      site.data['publications'] = papers

      papers.each do |paper|
        directory = File.join('publications', paper['key'])
        page = PageWithoutAFile.new(site, site.source, directory, 'index.html')
        page.data.merge!('layout' => 'paper', 'title' => paper['title'], 'description' => paper['description'], 'paper' => paper)
        site.pages << page
        add_export(site, "#{directory}/cite.bib", paper['bibtex'])
        add_export(site, "#{directory}/cite.ris", paper['ris'])
        add_export(site, "#{directory}/summary.md", markdown_record(paper))
      end

      add_export(site, 'publications.bib', papers.map { |paper| paper['bibtex'] }.join("\n"))
      catalog = {
        'version' => 1,
        'title' => "#{site.config['first_name']} #{site.config['last_name']} — publications",
        'url' => "#{site_base(site)}/publications/",
        'author' => owner_identity(site),
        'publications' => papers.map { |paper| paper.reject { |key, _| %w[bibtex ris schema month_number].include?(key) } }
      }
      add_export(site, 'publications.json', JSON.pretty_generate(catalog) + "\n")
    end

    private

    def site_base(site)
      site.config['url'].to_s.sub(%r{/$}, '') + site.config['baseurl'].to_s.sub(%r{/$}, '')
    end

    def clean(value)
      value.to_s.gsub(/[{}]/, '').gsub('\\%', '%').gsub('\\&', '&').gsub(/\s+/, ' ').strip
    end

    def field(entry, name)
      value = entry.field?(name) ? clean(entry[name]) : nil
      value unless value.to_s.empty?
    end

    def absolute_url(site, url)
      return nil if url.to_s.empty?
      return url if url.match?(%r{\Ahttps?://})

      "#{site_base(site)}/#{url.sub(%r{\A/+}, '')}"
    end

    def owner_identity(site)
      name = [site.config['first_name'], site.config['last_name']].compact.join(' ')
      identifier = site.config['orcid_id'].to_s.empty? ? "#{site_base(site)}/#person" : "https://orcid.org/#{site.config['orcid_id']}"
      { '@type' => 'Person', '@id' => identifier, 'name' => name, 'url' => "#{site_base(site)}/" }
    end

    def publication_kind(entry)
      # arXiv identifiers also occur on published papers; only a preprint venue
      # identifies an entry as a preprint. Do not infer peer-review from a DOI.
      venue = field(entry, :journal) || field(entry, :howpublished)
      return ['preprint', 'Preprint', 'preprint'] if venue.to_s.match?(/arxiv|biorxiv|techrxiv|preprints\.org/i)
      return ['software', 'Software release', 'released'] if field(entry, :abbr) == 'Software'

      case entry.type.to_s
      when 'inproceedings', 'conference' then ['conference-paper', 'Conference paper', 'published']
      when 'article' then ['journal-article', 'Journal article', 'published']
      when 'incollection', 'inbook' then ['book-chapter', 'Book chapter', 'published']
      when 'book' then ['book', 'Book', 'published']
      else ['other', 'Research output', 'unspecified']
      end
    end

    def paper_data(site, entry, raw_entry, filtered)
      key = entry.key.to_s
      raise "Unsafe publication key: #{key}" unless key.match?(/\A[\w.-]+\z/)

      research = site.data.fetch('research', {}).fetch('papers', {}).fetch(key, {})
      authors = entry.author ? entry.author.map { |name| clean(name.display_order) } : []
      month = field(entry, :month)
      month_number = month && (MONTHS.index(month.downcase[0, 3]).to_i + 1 if MONTHS.include?(month.downcase[0, 3]))
      month_number ||= month.to_i if month.to_s.match?(/\A(?:0?[1-9]|1[0-2])\z/)
      date = field(entry, :year).to_s
      date += format('/%02d', month_number) if month_number
      pages = field(entry, :pages).to_s.split(/-+|–/).map(&:strip)
      pdf = field(entry, :pdf)
      pdf = absolute_url(site, pdf.start_with?('/') ? pdf : "assets/pdf/#{pdf}") if pdf && !pdf.match?(%r{\Ahttps?://})
      abstract = field(entry, :abstract) || research['abstract']
      abstract_source = research['abstract_source'] && absolute_url(site, research['abstract_source'])
      kind, kind_label, status = publication_kind(entry)
      url = "#{site_base(site)}/publications/#{key}/"
      doi = field(entry, :doi)
      arxiv = field(entry, :arxiv)
      arxiv ||= field(entry, :eprint) if field(entry, :archiveprefix).to_s.casecmp('arxiv').zero?
      identifier = doi ? "https://doi.org/#{doi}" : arxiv ? "https://arxiv.org/abs/#{arxiv}" : url
      citation = raw_entry.dup
      filtered.each { |name| citation.delete(name) }
      description = research['summary'] || abstract || "#{field(entry, :title)}. #{authors.join(', ')}."
      description = description[0, 297].sub(/\s+\S*\z/, '') + '…' if description.length > 300

      paper = {
        'key' => key,
        'type' => entry.type.to_s,
        'bibliographic_type' => kind,
        'type_label' => kind_label,
        'publication_status' => status,
        'title' => field(entry, :title),
        'authors' => authors,
        'year' => field(entry, :year),
        'date' => date,
        'date_published' => date.tr('/', '-'),
        'month_number' => month_number,
        'venue' => field(entry, :booktitle) || field(entry, :journal) || field(entry, :howpublished),
        'series' => field(entry, :series),
        'publisher' => field(entry, :publisher),
        'volume' => field(entry, :volume),
        'issue' => field(entry, :number),
        'article_number' => field(entry, :articleno),
        'firstpage' => pages[0],
        'lastpage' => pages[1],
        'isbn' => field(entry, :isbn),
        'doi' => doi,
        'arxiv' => arxiv,
        'identifier' => identifier,
        'url' => url,
        'pdf' => pdf,
        'code' => field(entry, :code),
        'html' => field(entry, :html),
        'html_full_text' => absolute_url(site, research['html_full_text']),
        'source_url' => field(entry, :url),
        'bibtex_url' => "#{url}cite.bib",
        'ris_url' => "#{url}cite.ris",
        'markdown_url' => "#{url}summary.md",
        'abbr' => field(entry, :abbr),
        'award_name' => field(entry, :award_name),
        'keywords' => field(entry, :keywords),
        'topics' => research.fetch('topics', []),
        'summary' => research['summary'],
        'when_to_read' => research['when_to_read'],
        'abstract' => abstract,
        'abstract_source' => abstract_source,
        'questions' => research.fetch('questions', []),
        'tutorials' => related_tutorials(site, key),
        'description' => description,
        'bibtex' => citation.to_s.strip + "\n"
      }
      paper['ris'] = ris_record(paper, entry)
      paper['schema'] = scholarly_schema(site, paper)
      paper
    end

    def related_tutorials(site, key)
      site.posts.docs.select { |post| Array(post.data['related_papers']).include?(key) }
          .sort_by(&:date).reverse.map do |post|
        {
          'title' => post.data['title'],
          'url' => absolute_url(site, post.url),
          'description' => post.data['description']
        }
      end
    end

    def markdown_link(label, url)
      # Angle-bracket destinations preserve URLs containing parentheses.
      label = label.to_s.gsub(/[\\\[\]]/) { |character| "\\#{character}" }
      "[#{label}](<#{url}>)"
    end

    def markdown_record(paper)
      sections = [
        "# #{paper['title']}",
        'Publication summary and citation record; follow the source links for the original work.'
      ]
      metadata = [
        "Authors: #{paper['authors'].join('; ')}",
        "Year: #{paper['year']}",
        "Type: #{paper['type_label']}",
        "Publication status: #{paper['publication_status']}",
        "Paper page: #{paper['url']}",
        "Scholarly identifier: #{paper['identifier']}"
      ]
      metadata << "Venue or repository: #{paper['venue']}" if paper['venue']
      metadata << "DOI: #{paper['doi']}" if paper['doi']
      metadata << "arXiv: https://arxiv.org/abs/#{paper['arxiv']}" if paper['arxiv']
      metadata << "Award: #{paper['award_name']}" if paper['award_name']
      metadata << "Topics: #{paper['topics'].join('; ')}" unless paper['topics'].empty?
      sections << metadata.map { |line| "- #{line}" }.join("\n")

      links = [
        ['Full paper (HTML)', paper['html_full_text']],
        ['Read PDF', paper['pdf']],
        ['Paper online', paper['html']],
        ['Publication source', paper['source_url']],
        ['Code and resources', paper['code']]
      ].reject { |_, url| url.to_s.empty? }
      unless links.empty?
        sections << "## Source links\n\n" + links.map { |label, url| "- #{markdown_link(label, url)}" }.join("\n")
      end

      sections << "## Contribution summary\n\n#{paper['summary']}" if paper['summary']
      sections << "## When to read this work\n\n#{paper['when_to_read']}" if paper['when_to_read']
      if paper['abstract']
        abstract = "## Abstract\n\n#{paper['abstract']}"
        abstract += "\n\nAbstract source: #{paper['abstract_source']}" if paper['abstract_source']
        sections << abstract
      end

      unless paper['questions'].empty?
        questions = paper['questions'].map do |question|
          source = markdown_link(question.fetch('source_label'), question.fetch('source_url'))
          "### #{question.fetch('question')}\n\n#{question.fetch('answer')}\n\nSource: #{source}"
        end
        sections << ['## Questions about this work', *questions].join("\n\n")
      end

      unless paper['tutorials'].empty?
        tutorials = paper['tutorials'].map do |tutorial|
          link = "- #{markdown_link(tutorial['title'], tutorial['url'])}"
          link += " — #{tutorial['description']}" unless tutorial['description'].to_s.empty?
          link
        end
        sections << "## Tutorials and reading guides\n\n" + tutorials.join("\n")
      end

      citation_links = [markdown_link('Download BibTeX', paper['bibtex_url']), markdown_link('Download RIS', paper['ris_url'])]
      sections << "## Cite this work\n\n#{citation_links.join(' · ')}\n\n```bibtex\n#{paper['bibtex']}```"
      sections.join("\n\n") + "\n"
    end

    def scholarly_schema(site, paper)
      owner = owner_identity(site)
      authors = paper['authors'].map { |name| name == owner['name'] ? owner : { '@type' => 'Person', 'name' => name } }
      schema = {
        '@context' => 'https://schema.org',
        '@type' => paper['bibliographic_type'] == 'software' ? 'SoftwareSourceCode' : 'ScholarlyArticle',
        '@id' => paper['identifier'],
        'name' => paper['title'],
        'headline' => paper['title'],
        'author' => authors,
        'url' => paper['url'],
        'mainEntityOfPage' => paper['url'],
        'datePublished' => paper['date_published'],
        'creativeWorkStatus' => paper['publication_status'],
        'inLanguage' => site.config['lang'] || 'en'
      }
      if paper['venue'] && !%w[preprint software].include?(paper['bibliographic_type'])
        container_type = { 'journal-article' => 'Periodical', 'book-chapter' => 'Book' }.fetch(paper['bibliographic_type'], 'CreativeWork')
        schema['isPartOf'] = { '@type' => container_type, 'name' => paper['venue'] }
      end
      schema['publisher'] = { '@type' => 'Organization', 'name' => paper['publisher'] } if paper['publisher']
      schema['abstract'] = paper['abstract'] if paper['abstract']
      schema['description'] = paper['summary'] if paper['summary']
      schema['keywords'] = (paper['topics'] + paper['keywords'].to_s.split(/,\s*/)).uniq.reject(&:empty?)
      schema.delete('keywords') if schema['keywords'].empty?
      schema['identifier'] = { '@type' => 'PropertyValue', 'propertyID' => 'DOI', 'value' => paper['doi'] } if paper['doi']
      same_as = [paper['source_url'], paper['html'], paper['html_full_text']]
      same_as << "https://doi.org/#{paper['doi']}" if paper['doi']
      same_as << "https://arxiv.org/abs/#{paper['arxiv']}" if paper['arxiv']
      schema['sameAs'] = same_as.compact.uniq unless same_as.compact.empty?
      schema['encoding'] = { '@type' => 'MediaObject', 'contentUrl' => paper['pdf'], 'encodingFormat' => 'application/pdf' } if paper['pdf']
      schema['codeRepository'] = paper['code'] if paper['bibliographic_type'] == 'software' && paper['code']
      schema
    end

    def ris_record(paper, entry)
      type = { 'conference-paper' => 'CONF', 'journal-article' => 'JOUR', 'book-chapter' => 'CHAP',
               'book' => 'BOOK', 'preprint' => 'UNPB', 'software' => 'COMP' }.fetch(paper['bibliographic_type'], 'GEN')
      rows = [['TY', type], ['ID', paper['key']], ['TI', paper['title']]]
      entry.author&.each { |name| rows << ['AU', clean(name.sort_order)] }
      entry.editor&.each { |name| rows << ['ED', clean(name.sort_order)] }
      rows += [['PY', paper['year']], ['DA', paper['date']], ['T2', paper['venue']], ['VL', paper['volume']],
               ['IS', paper['issue']], ['SP', paper['firstpage']], ['EP', paper['lastpage']], ['PB', paper['publisher']],
               ['SN', paper['isbn']], ['DO', paper['doi']], ['UR', paper['identifier']], ['L1', paper['pdf']], ['AB', paper['abstract']]]
      paper['topics'].each { |topic| rows << ['KW', topic] }
      rows.reject { |_, value| value.to_s.empty? }.map { |tag, value| "#{tag}  - #{value.to_s.gsub(/\s+/, ' ')}" }.join("\n") + "\nER  - \n"
    end

    def add_export(site, path, content)
      site.static_files << PublicationExport.new(site, path, content)

      # Minifiers must never reinterpret BibTeX, RIS, JSON, or Markdown as HTML.
      minifier = site.config['jekyll-minifier'] ||= {}
      minifier['exclude'] = (Array(minifier['exclude']) + [path]).uniq
    end
  end
end
