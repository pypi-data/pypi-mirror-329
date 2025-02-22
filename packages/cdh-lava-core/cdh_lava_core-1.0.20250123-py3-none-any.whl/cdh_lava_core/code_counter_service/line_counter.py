import os
import datetime
from collections import defaultdict

class LineCounter:
    def __init__(self, directory):
        self.directory = directory
        self.total_files = 0
        self.total_code_lines = 0
        self.total_comment_lines = 0
        self.total_blank_lines = 0
        self.report_lines = []
        self.folder_summary = defaultdict(lambda: defaultdict(lambda: [0, 0, 0, 0]))  # [code, comment, blank, total]
        self.language_file_count = defaultdict(int)  # Track the number of files per language
        self.service_dir_count = 0

    def count_lines(self, file_path):
        code_lines, comment_lines, blank_lines = 0, 0, 0
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    stripped_line = line.strip()
                    if not stripped_line:
                        blank_lines += 1
                    elif stripped_line.startswith("#") or stripped_line.startswith("//"):
                        comment_lines += 1
                    else:
                        code_lines += 1
        except Exception as e:
            print(f"Could not read file {file_path}: {e}")
        return code_lines, comment_lines, blank_lines

    def is_binary_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                for block in iter(lambda: f.read(1024), b''):
                    if b'\0' in block:
                        return True
        except Exception as e:
            print(f"Could not check if file is binary {file_path}: {e}")
        return False

    def get_file_language(self, file_name):
        if file_name.endswith(".txt"):
            return "pip requirements"
        elif file_name.endswith(".csv"):
            return "CSV"
        elif file_name.endswith(".xlsx"):
            return "Excel"
        elif file_name.endswith(".py"):
            return "Python"
        elif file_name.endswith(".java"):
            return "Java"
        elif file_name.endswith(".js"):
            return "JavaScript"
        elif file_name.endswith(".html"):
            return "HTML"
        elif file_name.endswith(".css"):
            return "CSS"
        else:
            return "Unknown"

    def generate_report(self, print_details=False):
        self.report_lines.append("# Details")
        self.report_lines.append(f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.report_lines.append(f"**Directory:** {self.directory}\n")

        if not os.path.exists(self.directory):
            print(f"Directory '{self.directory}' does not exist.")
            return
        
        for root, dirs, files in os.walk(self.directory):
            # Skip __pycache__ directories
            dirs[:] = [d for d in dirs if d != '__pycache__']

            for dir in dirs:
                if 'service' in dir.lower():
                    self.service_dir_count += 1

            for file in files:
                file_path = os.path.join(root, file)
                if self.is_binary_file(file_path):
                    continue
                language = self.get_file_language(file)
                self.language_file_count[language] += 1
                code_lines, comment_lines, blank_lines = self.count_lines(file_path)
                total_lines = code_lines + comment_lines + blank_lines

                relative_path = file_path[len(self.directory)+1:]
                folder = os.path.dirname(relative_path)
                self.folder_summary[folder][language][0] += code_lines
                self.folder_summary[folder][language][1] += comment_lines
                self.folder_summary[folder][language][2] += blank_lines
                self.folder_summary[folder][language][3] += total_lines
                
                self.total_files += 1
                self.total_code_lines += code_lines
                self.total_comment_lines += comment_lines
                self.total_blank_lines += blank_lines

                if print_details:
                    self.report_lines.append(f"| {relative_path} | {language} | {code_lines:,} | {comment_lines:,} | {blank_lines:,} | {total_lines:,} |")
        
        if print_details:
            self.report_lines.append("\n## Folder Summary")
        
        self.report_lines.append("| Path | Language | Code | Comment | Blank | Total |")
        self.report_lines.append("| --- | --- | --- | --- | --- | --- |")
        
        folder_hierarchy = defaultdict(lambda: defaultdict(dict))  # Nested dictionaries to create hierarchy
        
        for folder, languages in self.folder_summary.items():
            parts = folder.split(os.sep)
            current_level = folder_hierarchy
            for part in parts:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
            for language, counts in languages.items():
                current_level[language] = counts

        def print_folder_summary(level, depth=0):
            sorted_folders = sorted(level.keys())
            for folder in sorted_folders:
                languages = level[folder]
                if isinstance(languages, dict):
                    bold_folder = f"{'&nbsp;' * depth * 4}**{folder}**"
                    self.report_lines.append(f"| {bold_folder} |  |  |  |  |  |")
                    print_folder_summary(languages, depth + 1)
                else:
                    counts = languages
                    indented_folder = f"{'&nbsp;' * (depth + 1) * 4}{folder}"
                    self.report_lines.append(f"| {indented_folder} | {counts[0]:,} | {counts[1]:,} | {counts[2]:,} | {counts[3]:,} |")
        
        print_folder_summary(folder_hierarchy)

        self.report_lines.append("\n## Overall Summary")
        self.report_lines.append(f"**Total files:** {self.total_files:,}")
        self.report_lines.append(f"**Total code lines:** {self.total_code_lines:,}")
        self.report_lines.append(f"**Total comments:** {self.total_comment_lines:,}")
        self.report_lines.append(f"**Total blank lines:** {self.total_blank_lines:,}")
        self.report_lines.append(f"**Total lines:** {self.total_code_lines + self.total_comment_lines + self.total_blank_lines:,}")
        self.report_lines.append(f"**Total directories with 'service' in their name:** {self.service_dir_count:,}")

        overall_by_type = defaultdict(lambda: [0, 0, 0, 0])  # [code, comment, blank, total]

        for folder, languages in self.folder_summary.items():
            for language, counts in languages.items():
                overall_by_type[language][0] += counts[0]
                overall_by_type[language][1] += counts[1]
                overall_by_type[language][2] += counts[2]
                overall_by_type[language][3] += counts[3]

        self.report_lines.append("\n## Overall Summary by Type")
        self.report_lines.append("| Language | Files | Code | Comment | Blank | Total |")
        self.report_lines.append("| --- | --- | --- | --- | --- | --- |")
        for language, counts in sorted(overall_by_type.items()):
            file_count = self.language_file_count[language]
            self.report_lines.append(f"| {language} | {file_count:,} | {counts[0]:,} | {counts[1]:,} | {counts[2]:,} | {counts[3]:,} |")

        report_content = "\n".join(self.report_lines)
        print(report_content)

        # Save the report to the project root directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        report_path = os.path.join(project_root, "report.md")
        with open(report_path, "w", encoding="utf-8") as report_file:
            report_file.write(report_content)
            
        print(f"Report saved to {report_path}")

        return report_path

# Example usage
if __name__ == "__main__":
    directory_path = "/home/developer/projects/cdh-lava-core/cdh_lava_core"
    line_counter = LineCounter(directory_path)
    line_counter.generate_report(print_details=True)
