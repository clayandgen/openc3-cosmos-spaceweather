# encoding: ascii-8bit

# Create the overall gemspec
Gem::Specification.new do |s|
  s.name = 'openc3-cosmos-spaceweather'
  s.summary = 'Space Weather Alerts'
  s.description = <<-EOF
    NOAA SWPC API Plugin to receive and view Space Weather Alerts
  EOF
  s.license = 'MIT'
  s.authors = ['Clay Kramp']
  s.email = ['clay@openc3.com']
  s.homepage = 'https://github.com/clayandgen/openc3-cosmos-spaceweather'
  s.version = "1.0.0"
  s.platform = Gem::Platform::RUBY

  s.metadata = {
    "source_code_uri" => "https://github.com/clayandgen/openc3-cosmos-spaceweather",
    "openc3_cosmos_minimum_version" => "5.0.0",
    "openc3_store_access_type" => "public",
    "openc3_store_keywords" => "Space Weather, NOAA"
  }

  if ENV['VERSION']
    s.version = ENV['VERSION'].dup
  else
    time = Time.now.strftime("%Y%m%d%H%M%S")
    s.version = '0.0.0' + ".#{time}"
  end

  s.files = Dir.glob("{targets,lib,public,tools,microservices}/**/*") + %w(Rakefile README.md LICENSE.md plugin.txt)
end
