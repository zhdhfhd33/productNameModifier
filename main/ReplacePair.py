# 작더라도 클래스를 선언하는게 유지보수에 매우 편하다.
# 딕셔너리는 매우 불안하고 불편. 매번 키 확인해야한다. 객체를 만들면 에러도 알아서 잡아준다.
class ReplacePair():
    def __init__(self, target, replace):
        self.target = target
        self.replace = replace

