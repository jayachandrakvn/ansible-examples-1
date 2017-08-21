require 'yaml'
#
# The purpose of this code is not exactly to "demo" anything
# to the public, but provide the internal mechanism for the
# developer of those example, so each example can be added
# as a single file under 'playbooks/examples' folder.
#
# The script will scan that folder and will make a list of all
# examples present dynamically (opposed to manually adding each
# example to some sort of static list).
#
# But feel free to see how it works and reuse its pieces.
#
module FsTree
  class FsTreeRoot
    attr_reader :root_folder, :sections

    def dir_list(dir)
      Dir.chdir(dir)
      Dir.glob('*').select do |f|
        File.directory? f
      end.sort
    end

    def initialize(root)
      @root_folder = root
      @sections = dir_list(root)
    end
  end

  class FsTreeFiles
    attr_reader :section_path, :filenames

    def file_list(dir)
      Dir.chdir(dir)
      Dir.glob('*.yaml').select {|f| File.file? f}
    end

    def initialize(section_path)
      @section_path = section_path
      @filenames = file_list(section_path)
    end

    def filename2hostname(filename)
      filename.gsub(/\.yaml$/, '')
    end

    def hostnames
      filenames.map { |file| filename2hostname(file) }.sort
    end

    def hostvars
      filenames.inject({}) do |tmphash, filename|
        hostname = filename2hostname(filename)
        tmphash[hostname] = YAML.load(File.read(section_path + '/' + filename))
        tmphash
      end
    end
  end

  class FsTree
    attr_reader :root_obj, :file_examples

    def initialize(root)
      @root_obj = FsTreeRoot.new(root)
      @file_examples = root_obj.sections.inject({}) do |tmphash, section|
        tmphash[section] = FsTreeFiles.new(root + '/' + section)
        tmphash
      end
    end

    def generate_each_section
      root_obj.sections.inject({}) do |tmphash, section|
        tmphash[section] = file_examples[section].hostnames
        tmphash
      end
    end

    def all_sections
      generate_each_section.map {|_k, v| v }.flatten.uniq.sort
    end

    def all_examples
      { 'all' => all_sections }.merge(generate_each_section)
    end

    def all_hosts_meta
      root_obj.sections.inject({}) do |tmphash, section|
        tmphash.merge!(file_examples[section].hostvars)
        tmphash
      end
    end
  end
end
