from src.analyzer.lexical.const import TableOut, TableLexem, State
from src.analyzer.lexical.reader import Reader
from src.analyzer.lexical.sub.delimiter.analyzer import DelimiterAnalyzer
from src.analyzer.lexical.sub.sub import SubAnalyzer



class NumberAnalyzer(SubAnalyzer):
    def __init__(self, reader: Reader):
        super().__init__(reader)
        self._reader.state = State.NUMBER

    def analyze(self) -> Reader:
        self._reader.nill()
        if self._reader.check_pattern("[0-1]"):
            self._reader = BinaryNumberAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("[2-7]"):
            self._reader = OctNumberAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("[8-9]"):
            self._reader = DecimalAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("[0-9A-Fa-f]"):
            self._reader = HexAnalyzer(self._reader).analyze()
        return self._reader

class BinaryNumberAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:
        while self._reader.has_next():
            self._reader.next()
            if self._reader.check_pattern("[0-1]"):
                self._reader.add()
            else:
                break

        if self._reader.check_pattern('[Bb]'):
            self._reader.add()
            if self._reader.has_next():
                self._reader.next()
                if self._reader.check_pattern('[0-9A-Fa-f]'):
                    return HexAnalyzer(self._reader).analyze()
                elif self._reader.check_pattern("[Hh]"):
                    return HexEndAnalyzer(self._reader).analyze()
                else:
                    self._reader.state = State.ERROR
                    return self._reader
            z = self._reader.put(TableOut.TN)
            self._reader.out(TableLexem.TN, z)

            if self._reader.current_last():
                self._reader.gc.ch = ""

            return self._reader

        elif self._reader.check_pattern("[2-7]"):
            return OctNumberAnalyzer(self._reader).analyze()

        elif self._reader.check_pattern("[8-9]"):
            return DecimalAnalyzer(self._reader).analyze()

        elif self._reader.check_pattern("[ACFacf]"):
            return HexAnalyzer(self._reader).analyze()

        elif self._reader.check_pattern('\\.'):
            return FloatNumberAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern('[Ee]'):
            return ExponentAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern('[Oo]'):
            self._reader.add()
        elif self._reader.check_pattern('[Dd]'):
            self._reader.add()
        elif self._reader.check_pattern('[Hh]'):
            return HexEndAnalyzer(self._reader).analyze()

        if not self._reader.is_delimiter() and not self._reader.check_pattern('[0-1]'):
            self._reader.state = State.ERROR
            return self._reader

        z = self._reader.put(TableOut.TN)
        self._reader.out(TableLexem.TN, z)

        if self._reader.current_last():
            self._reader.gc.ch = ""

        return self._reader

class FloatNumberAnalyzer(NumberAnalyzer):

    def __init__(self, reader: Reader):
        # self._reader.state = State.FLOAT
        super().__init__(reader)

    def analyze(self) -> Reader:
        # if self._reader.has_next():
        #     self._reader.next()

        added = False
        while self._reader.has_next():
            self._reader.next()
            if self._reader.check_pattern("[0-9]"):
                self._reader.add()
                added = True
            else:
                break

        if not added:
            self._reader.state = State.ERROR
            return self._reader

        # while self._reader.check_pattern("[0-9]"):
        #     self._reader.add()
        #     if self._reader.current_last():
        #         self._reader.gc.ch = ""
        #         break
        #     else:
        #         self._reader.next()

        if self._reader.check_pattern("[Ee]"):
            return FloatExponentAnalyzer(self._reader).analyze()

        if not self._reader.check_pattern("[0-9]") and not self._reader.is_delimiter():
            self._reader.state = State.ERROR
            return self._reader



        z = self._reader.put(TableOut.TN)
        self._reader.out(TableLexem.TN, z)

        if self._reader.current_last():
            self._reader.gc.ch = ""

        return self._reader


class FloatExponentAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:

        if self._reader.has_next():
            self._reader.next()
            if self._reader.check_pattern("[+-0-9]"):
                self._reader.add()
                self._analyze()
            else:
                self._reader.state = State.ERROR
        else:
            self._reader.state = State.ERROR
        return self._reader

    def _analyze(self):
        while self._reader.gc.has_next():
            self._reader.next()
            if self._reader.check_pattern("[0-9]"):
                self._reader.add()
            else:
                break

        z = self._reader.put(TableOut.TN)
        self._reader.out(TableLexem.TN, z)

        if self._reader.current_last() and not self._reader.is_delimiter():
            self._reader.gc.ch = ""

class OctNumberAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:
        while self._reader.has_next():
            self._reader.next()
            if self._reader.check_pattern("[0-7]"):
                self._reader.add()
            else:
                break
        if self._reader.check_pattern("[8-9]"):
            return DecimalAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("\\."):
            return FloatNumberAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("[Ee]"):
            return ExponentAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("[Dd]"):
            return NumberEndAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("[ACFacf]"):
            return HexAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("[Hh]"):
            return HexEndAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("[Oo]"):
            return OctEndAnalyzer(self._reader).analyze()

        if self._reader.is_delimiter():
            return DelimiterAnalyzer(self._reader).analyze()

        if not self._reader.is_delimiter() and not self._reader.check_pattern('[0-7]'):
            self._reader.state = State.ERROR
            return self._reader

        z = self._reader.put(TableOut.TN)
        self._reader.out(TableLexem.TN, z)
        self._reader.nill()

        if self._reader.current_last():
            self._reader.gc.ch = ""

        return self._reader


class DecimalAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:
        while self._reader.has_next():
            self._reader.next()
            if self._reader.check_pattern("[0-9]"):
                self._reader.add()
            else:
                break

        if self._reader.check_pattern("[Hh]"):
            self._reader.add()
        elif self._reader.check_pattern("[Ee]"):
            return ExponentAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("\\."):
            return FloatNumberAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("[ACFacf]"):
            return HexAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern("[Dd]"):
            self._reader.add()
            if self._reader.has_next():
                self._reader.next()
                if self._reader.check_pattern("[A-Fa-f0-9]"):
                    return HexAnalyzer(self._reader).analyze()
                elif self._reader.check_pattern("[Hh]"):
                    self._reader.add()
        # else:
        #     self._reader.state = State.ERROR
        #     return self._reader

        z = self._reader.put(TableOut.TN)
        self._reader.out(TableLexem.TN, z)

        if self._reader.current_last():
            self._reader.gc.ch = ""

        return self._reader


class HexAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:
        while self._reader.has_next():
            self._reader.next()
            if self._reader.check_pattern("[0-9A-Fa-f]"):
                self._reader.add()
            else:
                break
        if self._reader.check_pattern('[Hh]'):
            return HexEndAnalyzer(self._reader).analyze()
            # self._reader.add()
            # if self._reader.has_next():
            #     self._reader.next()
            #     if not self._reader.is_delimiter():
            #         self._reader.state = State.ERROR
            #         return self._reader

            # z = self._reader.put(TableOut.TN)
            # self._reader.out(TableLexem.TN, z)
        else:
            self._reader.state = State.ERROR

        if self._reader.current_last():
            self._reader.gc.ch = ""

        return self._reader



class ExponentAnalyzer(SubAnalyzer):
    def analyze(self) -> Reader:

        if self._reader.has_next():
            self._reader.next()
        else:
            self._reader.state = State.ERROR
            return self._reader

        if self._reader.check_pattern("[+-]"):
            self._reader.add()
            while self._reader.has_next():
                self._reader.next()
                if self._reader.check_pattern("[0-9]"):
                    self._reader.add()
                else:
                    break

            if self._reader.has_next():
                self._reader.state = State.ERROR
                return self._reader

            z = self._reader.put(TableOut.TN)
            self._reader.out(TableLexem.TN, z)


        elif self._reader.check_pattern("[0-9]"):
            self._reader.add()
            while self._reader.gc.has_next():
                self._reader.next()
                if self._reader.check_pattern("[0-9]"):
                    self._reader.add()
                else:
                    break
            if self._reader.check_pattern("[A-Fa-f]"):
                return HexAnalyzer(self._reader).analyze()
            elif self._reader.check_pattern("[Hh]"):
                # self._reader.add()
                return HexAnalyzer(self._reader).analyze()
            if self._reader.white_spaces():
                z = self._reader.put(TableOut.TN)
                self._reader.out(TableLexem.TN, z)
            else:
                self._reader.state = State.ERROR
        elif self._reader.check_pattern("[A-Fa-f]"):
            return HexAnalyzer(self._reader).analyze()
        elif self._reader.check_pattern('[Hh]'):
            self._reader.add()
            if self._reader.has_next():
                self._reader.next()
                if not self._reader.is_delimiter():
                    self._reader.state = State.ERROR
                    return self._reader
            z = self._reader.put(TableOut.TN)
            self._reader.out(TableLexem.TN, z)
        else:
            self._reader.state = State.ERROR

        if self._reader.current_last():
            self._reader.gc.ch = ""

        return self._reader

class HexEndAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:
        if self._reader.has_next():
            self._reader.next()
            if not self._reader.is_delimiter():
                self._reader.state = State.ERROR
                return self._reader
        z = self._reader.put(TableOut.TN)
        self._reader.out(TableLexem.TN, z)

        if self._reader.current_last():
            self._reader.gc.ch = ""

        return self._reader

class OctEndAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:
        if self._reader.has_next():
            self._reader.next()
            if not self._reader.is_delimiter():
                self._reader.state = State.ERROR
                return self._reader
        z = self._reader.put(TableOut.TN)
        self._reader.out(TableLexem.TN, z)

        if self._reader.current_last():
            self._reader.gc.ch = ""

        return self._reader

class NumberEndAnalyzer(NumberAnalyzer):
    def analyze(self) -> Reader:
        if self._reader.has_next():
            self._reader.next()
            if not self._reader.is_delimiter():
                self._reader.state = State.ERROR
                return self._reader
        z = self._reader.put(TableOut.TN)
        self._reader.out(TableLexem.TN, z)

        if self._reader.current_last():
            self._reader.gc.ch = ""

        return self._reader