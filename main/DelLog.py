
class DelLog():
    def __init__(self, idx, content, regexp):
        self.regexp = regexp
        self.content = content
        self.idx = idx

    def __str__(self):
        return f'regexp : {self.regexp}    content : {self.content}    idx : {self.idx}    xlsIdx : {self.getXlsIdx()}'


    def getXlsIdx(self):
        return self.idx + 2

