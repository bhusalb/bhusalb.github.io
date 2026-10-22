# Generates one landing page per bibliography entry at /publications/<key>/.
# Each page carries Google Scholar (Highwire Press) citation_* meta tags and
# schema.org ScholarlyArticle data so that Google Scholar can index the paper
# and attach the self-hosted PDF as an additional full-text version.
# See https://scholar.google.com/intl/en/scholar/inclusion.html#indexing

require 'bibtex'

module Jekyll
  class PaperPagesGenerator < Generator
    safe true
    priority :low

    MONTHS = %w[jan feb mar apr may jun jul aug sep oct nov dec].freeze

    def generate(site)
      scholar = site.config['scholar'] || {}
      bib_path = File.join(site.source, scholar['source'] || '_bibliography', scholar['bibliography'] || 'papers.bib')
      return unless File.exist?(bib_path)

      # Strip the Jekyll front matter before parsing
      source = File.read(bib_path).sub(/\A---\s*\n.*?\n---\s*\n/m, '')
      bibliography = BibTeX.parse(source, filter: :latex)
      raw_bibliography = BibTeX.parse(source)
      filtered = site.config['filtered_bibtex_keywords'] || []

      bibliography.each_entry do |entry|
        page = PageWithoutAFile.new(site, site.source, File.join('publications', entry.key.to_s), 'index.html')
        paper = paper_data(site, entry, raw_bibliography[entry.key], filtered)
        page.data['layout'] = 'paper'
        page.data['title'] = paper['title']
        page.data['description'] = paper['description']
        page.data['paper'] = paper
        site.pages << page
      end
    end

    private

    def clean(value)
      value.to_s.gsub(/[{}]/, '').gsub('\\%', '%').gsub('\\&', '&').gsub(/\s+/, ' ').strip
    end

    def field(entry, name)
      entry.field?(name) ? clean(entry[name]) : nil
    end

    def paper_data(site, entry, raw_entry, filtered)
      base = site.config['url'].to_s + site.config['baseurl'].to_s.chomp('/')
      authors = entry.author ? entry.author.map { |n| clean("#{n.first} #{n.last}") } : []
      month = field(entry, :month)
      month_num = month && (MONTHS.index(month.downcase[0, 3]) || (month.to_i - 1))
      date = field(entry, :year).to_s
      date += format('/%02d', month_num + 1) if month_num && month_num >= 0
      pages = field(entry, :pages).to_s.split(/-+|–/).map(&:strip)
      pdf = field(entry, :pdf)
      pdf = "#{base}/assets/pdf/#{pdf}" if pdf && !pdf.include?('://')
      abstract = field(entry, :abstract)

      # BibTeX shown to visitors (unconverted LaTeX), without the website-only fields
      bibtex = raw_entry.to_s.lines.reject { |l| (filtered + ["month_numeric"]).any? { |k| l =~ /^\s*#{k}\s*=/ } }.join
      bibtex = bibtex.sub(/,(\s*\}\s*)\z/, '\1')

      {
        'key' => entry.key.to_s,
        'type' => entry.type.to_s,
        'title' => field(entry, :title),
        'authors' => authors,
        'year' => field(entry, :year),
        'date' => date,
        'venue' => field(entry, :booktitle) || field(entry, :journal) || field(entry, :howpublished),
        'series' => field(entry, :series),
        'publisher' => field(entry, :publisher),
        'volume' => field(entry, :volume),
        'issue' => field(entry, :number),
        'firstpage' => pages[0],
        'lastpage' => pages[1],
        'isbn' => field(entry, :isbn),
        'doi' => field(entry, :doi),
        'arxiv' => field(entry, :arxiv),
        'pdf' => pdf,
        'code' => field(entry, :code),
        'html' => field(entry, :html),
        'abbr' => field(entry, :abbr),
        'award_name' => field(entry, :award_name),
        'keywords' => field(entry, :keywords),
        'abstract' => abstract,
        'description' => abstract ? abstract[0, 300].sub(/\s+\S*\z/, '') + '...' : "#{field(entry, :title)}. #{authors.join(', ')}.",
        'bibtex' => bibtex
      }
    end
  end
end
