require "pathname"

module FsTree
  class FsTree
    attr_reader :root_folder, :sections

    def initialize(root)
      @root_folder = root
      @sections = dir_list(root)
    end

    def dir_list(dir)
      Dir.chdir(dir)
      Dir.glob('*').select do |f|
        File.directory? f
      end.sort
    end

    def file_list(dir)
      Dir.chdir(dir)
      Dir.glob('*.yaml').select {|f| File.file? f}.map do |f|
        f.gsub(/\.yaml$/, '')
      end.sort
    end

    def generate_each_section
      new_hash = {}
      sections.each do |section|
        new_hash[section] = file_list(root_folder + '/' + section)
      end
      new_hash
    end

    def all_sections
      generate_each_section.map {|_k, v| v }.flatten.uniq.sort
    end

    def all_examples
      { 'all' => all_sections }.merge(generate_each_section)
    end
  end
end
