# encoding: utf-8
import io



class DiffParser(object):

    _DIFF_SYMBOLS = ("diff", "---", "+++", "@@")
    _PARSED_DIFFS = {}
    start_line = 0
    diff_name = None
    place = None

    def __init__(self, diff):
        if not isinstance(diff, unicode):
            raise UnicodeError('No unicode diff found.')
        self.diff = io.StringIO(diff)

    def _line_nums(self, line):
        start = line[line.find('-')+1:line.find(',')]
        try:
            int(start)
        except ValueError:
            start = line[line.find('-')+1:line.find('-')+1+line[line.find('-'):].find(' ')]
        # self._PARSED_DIFFS[self.diff_name].setdefault('chunks', {}).setdefault('places', []).append(line[:line.rfind('@@')+2])
        first = line.replace(line[:line.rfind('@@')+2], '')

        if len(first) != 1:
            res = {'number': int(start), 'line': first}
            self._PARSED_DIFFS[self.diff_name].setdefault('chunks', {}).setdefault('content', []).append(res)
        dogs = line[:line.rfind('@@')+2]

        #self._PARSED_DIFFS[self.diff_name].setdefault('chunks', {}).setdefault('places', []).append(dogs)

        removed = dogs[dogs.find('-')+1:dogs.find('+')].strip()
        added = dogs[dogs.find('+')+1:].strip('@').strip()
        removed = removed[:removed.find(',')]
        added = added[:added.find(',')]
        try:
            removed = int(removed)
            added = int(added)
            if removed <= added:
                self.start_line = int(removed)
            else:
                self.start_line = int(added)
        except ValueError:
            pass

        self._PARSED_DIFFS[self.diff_name]['start_line'] = int(start)

    def _hanlder(self, line):
        try:
             line_starts = line.split()[0]
        except IndexError:
            pass
        else:
            if line.startswith('diff'):
                self._PARSED_DIFFS.setdefault(line, {})
                self.diff_name = line

            # Append extended diff content
            if line[:1].isalpha() and line_starts not in self._DIFF_SYMBOLS:
                self._PARSED_DIFFS[self.diff_name].setdefault('extended', []).append(line)

            # Append filename
            if line.startswith("---") or line.startswith("+++"):
                if not '/dev/null' in line:
                    filename = line.split()[1][1:]
                    self._PARSED_DIFFS[self.diff_name].setdefault('filename', filename)

            # And some chunks
            if line.startswith("@@"):
                self._PARSED_DIFFS[self.diff_name].setdefault('chunks', {}).setdefault(line, {})
                self.place = line
                self._line_nums(line)

            if line_starts not in self._DIFF_SYMBOLS and not line[:1].isalpha():
                res = {'number': self.start_line, 'line': line}
                self._PARSED_DIFFS[self.diff_name]['chunks'][self.place].setdefault('content', []).append(res)
                self.start_line += 1

    def _format_diff(self):
        diff = ""
        for line in self.diff.readlines():
            if line.startswith("@@") and not line.endswith("@@\n"):
                self._hanlder(line[:line.rfind("@@")+2] + "\n")
                self._hanlder(line[line.rfind("@@ ")+2:])
            else:
                self._hanlder(line)
        return diff

    def parse(self):
        self._format_diff()
        return self._PARSED_DIFFS