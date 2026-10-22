#!/usr/bin/env ruby
# Integration checks for the rendered site. Run after `bundle exec jekyll build`.
require 'json'
require 'nokogiri'
require 'uri'
require 'yaml'
require 'bibtex'

root = File.expand_path(ARGV.fetch(0, '_site'))
config = YAML.load_file('_config.yml')
origin = config.fetch('url') + config.fetch('baseurl', '').to_s
errors = []
check = ->(condition, message) { errors << message unless condition }
catalog = JSON.parse(File.read(File.join(root, 'publications.json')))
papers = catalog.fetch('publications')
check.call(papers.any?, 'Publication catalog must not be empty')
check.call(papers.map { |p| p.fetch('key') }.uniq.size == papers.size, 'Duplicate publication keys')

paths = ['index.html', 'research/index.html', 'publications/index.html', 'blog/index.html', 'cv/index.html']
paths += Dir.glob(File.join(root, 'blog', '**', 'index.html')).map { |f| f.delete_prefix(root + '/') }
paths += papers.map { |p| "publications/#{p.fetch('key')}/index.html" }
paths.uniq.each do |path|
  file = File.join(root, path)
  unless File.file?(file)
    errors << "Missing page: #{path}"
    next
  end
  doc = Nokogiri::HTML(File.read(file))
  canonical = doc.css('link[rel="canonical"]')
  expected = origin + '/' + path.delete_suffix('index.html')
  check.call(canonical.size == 1 && canonical.first['href'] == expected, "Invalid canonical: #{path}")
  check.call(doc.at_css('meta[property="og:url"]')&.[]('content') == expected, "OpenGraph URL differs: #{path}")
  check.call(!doc.at_css('meta[name="robots"]')&.[]('content').to_s.include?('noindex'), "Research page is noindex: #{path}")
  check.call(doc.css('h1').size == 1, "Expected one main heading: #{path}")
  schema_types = []
  doc.css('script[type="application/ld+json"]').each do |script|
    begin
      schema_types << JSON.parse(script.content).fetch('@type')
    rescue JSON::ParserError => e
      errors << "Invalid JSON-LD: #{path}: #{e.message}"
    end
  end
  expected_types = if path == 'index.html'
                     %w[Person WebSite]
                   elsif path.match?(%r{\Ablog/\d{4}/[^/]+/index\.html\z})
                     ['BlogPosting']
                   elsif path.match?(%r{\Apublications/[^/]+/index\.html\z})
                     paper = papers.find { |p| path == "publications/#{p.fetch('key')}/index.html" }
                     [paper.fetch('bibliographic_type') == 'software' ? 'SoftwareSourceCode' : 'ScholarlyArticle']
                   else
                     ['WebPage']
                   end
  check.call((expected_types - schema_types).empty?, "Missing structured data #{expected_types.join(', ')}: #{path}")
  if path == 'research/index.html'
    topics = YAML.load_file('_data/research.yml').fetch('topics')
    topics.each do |topic|
      section = doc.at_css("section##{topic.fetch('id')}")
      check.call(section && section.css('h3 a').size == topic.fetch('papers').size, "Missing research summaries: #{topic.fetch('id')}")
    end
  end
  # Check local navigation, downloads, images, and script/style dependencies.
  doc.css('[href], [src]').each do |node|
    value = node['href'] || node['src']
    next if value.nil? || value.empty? || value.start_with?('#', 'mailto:', 'tel:', 'data:', 'javascript:')
    begin
      target = URI.join(expected, value)
      next unless target.host == URI(origin).host
      relative = URI::DEFAULT_PARSER.unescape(target.path).delete_prefix(config.fetch('baseurl', '').to_s).sub(%r{\A/}, '')
      destination = File.join(root, relative)
      destination = File.join(destination, 'index.html') if target.path.end_with?('/') || File.directory?(destination)
      check.call(File.file?(destination), "Broken local link on #{path}: #{value}")
    rescue URI::InvalidURIError
      errors << "Invalid URL on #{path}: #{value}"
    end
  end
end

papers.each do |paper|
  key = paper.fetch('key')
  path = "publications/#{key}"
  doc = Nokogiri::HTML(File.read(File.join(root, path, 'index.html')))
  check.call(doc.at_css('meta[name="citation_title"]')&.[]('content') == paper.fetch('title'), "Citation title differs: #{key}")
  check.call(doc.css('meta[name="citation_author"]').map { |n| n['content'] } == paper.fetch('authors'), "Citation authors differ: #{key}")
  bib = BibTeX.parse(File.read(File.join(root, path, 'cite.bib')))
  check.call(bib.entries.size == 1 && bib[key], "Invalid BibTeX download: #{key}")
  ris = File.read(File.join(root, path, 'cite.ris'))
  check.call(ris.start_with?('TY  - ') && ris.include?('ER  -'), "Invalid RIS download: #{key}")
end
all_bib = BibTeX.parse(File.read(File.join(root, 'publications.bib')))
check.call(all_bib.entries.size == papers.size, 'Combined BibTeX does not match publication catalog')
sitemap = Nokogiri::XML(File.read(File.join(root, 'sitemap.xml')))
locations = sitemap.xpath('//*[local-name()="loc"]').map(&:text)
paths.uniq.each do |path|
  check.call(locations.include?(origin + '/' + path.delete_suffix('index.html')), "Missing from sitemap: #{path}")
end
check.call(locations.none? { |u| u.match?(%r{/404\.html|/assets/|/projects/|/news/|/blog/20(15|18|20|21|22|23|24)/|\.(bib|ris|json|txt)\z}) }, 'Sitemap contains examples or non-content exports')
feed = Nokogiri::XML(File.read(File.join(root, 'feed.xml')))
check.call(feed.errors.none?, 'Invalid RSS/Atom feed')
entries = feed.xpath('//*[local-name()="entry"]')
check.call(entries.size >= 3, 'Research tutorials missing from feed')
check.call(entries.none? { |e| e.at_xpath('./*[local-name()="title"]')&.text.to_s.match?(/a post with|al-folio/i) }, 'Theme demos remain in feed')
%w[llms.txt llms-full.txt robots.txt publications.json publications.bib].each do |path|
  text = File.read(File.join(root, path))
  check.call(!text.include?('<html'), "HTML-wrapped export: #{path}")
  unless path.end_with?('.bib') # Nested BibTeX braces are valid, not Liquid.
    check.call(!text.include?('{{') && !text.include?('{%'), "Unrendered export: #{path}")
  end
end
check.call(File.binread(File.join(root, 'assets/pdf/CV.pdf'), 5) == '%PDF-', 'CV PDF was overwritten by an HTML page')
abort errors.uniq.join("\n") unless errors.empty?
puts "Research site checks passed: #{papers.size} publications, #{paths.uniq.size} pages, #{entries.size} feed entries."
