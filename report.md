# Report for Wang's Algorithm, Discrete Math I

## 1. 项目结构

```
wangs_algorithm
├─ .gitignore
├─ example-input.txt
├─ LICENSE
├─ README.md
├─ report.md
├─ requirements.txt
├─ setup.py
├─ test.py
├─ wangs_algorithm
│  ├─ data_types.py
│  ├─ deduction.py
│  ├─ preprocessing.py
│  └─ __init__.py
└─ readme
   └─ README.zh_cn.md
```

## 2. 代码设计

### 2.1 `./wangs_algorithm/__init__.py`

用于输出对外接口.

### 2.2 `./wangs_algorithm/data_types.py`

存放了算法实现所使用的两种基本类型`Operator`和`Statement`.

```python
class Operator(Enum):
    NOT = 1
    WEDGE = 2
    VEE = 3
    RIGHTARROW = 4
    LEFTRIGHTARROW = 5
    DEFAULT = 6
```

`Operator`类包括联结词，和一个默认值（用于赋给原子命题）.

```python
class Statement:
    def __init__(self) -> None:
        self.is_not: bool = False
        self.is_single: bool = True
        self.optr_type: Operator = Operator.DEFAULT
        self.content: str = ""
        self.sub_statements: list = list()
```

`Statement`类的属性有：
1. `is_not`：是否有否定联结词
2. `is_single`：是否为原子命题
3. `operator_type`：联结词类型，对于原子命题而言即为Operator.DEFAULT（这个属性的创建原因是因为在语法规则中，我们只允许一个命题中存在最多一种联结词）
4. `content`：原子命题的符号，若为复合命题则为空字符串
5. `sub_statements`：子命题，若为原子命题则为空列表

### 2.3 `./wangs_algorithm/preprocessing.py`

`check_and_parse_input`函数对输入字符串进行解析的同时，也检查其格式是否正确，若格式错误则调用`format_error`直接退出. 其遵循的语法规则请见`README.md`. 

总体思路是构造一个`stack`，遍历输入字符串：
1. 首先检查字符是否为合法字符，否则退出
2. 其次，根据该字符类型检查`stack`内存放的上一个`item`是否为合法，否则退出
3. 然后根据不同字符类型进行执行，多数情况下都是向`stack`内压入内容。这里只简要说明遇到右括号时的特殊情况：一直弹出`stack`内容直至弹出上一个左括号，然后检查左右括号内的部分是否合法，将其内容全部塞入某个`Statement`，然后压入栈

由于该函数较为复杂，不进行逐行解释.

### 2.4 `./wangs_algorithm/deduction.py`

对初始命题进行归结推理.

这里简要介绍遍历思路：
1. 遍历的数据结构为`list[list[list[Statement]]]`，最外层的`list`相当于是多组相继式（因为推理过程中相继式数量很可能会增加），中间一层`list`相当于是前件与后件，最后一层`list`分别用于存放前件与后件的各个子命题
2. 每次遍历，依序检查每个子命题是否有否定联结词，是否为原子命题. 若是，则根据归结规则改变原数据结构，然后`break`，进入下一个循环（不继续当前循环的原因是数据结构已发生改变，因此原有的索引会失效）
3. 遍历结束后检查各相继式前件与后件是否含有公共原子命题.

## 3. 测试

## 3.1 永真式

三段论

```
# python ./test.py --showsteps
Please enter your statement: ((P->Q)/\(Q->R))->(P->R)
Deduction starts.

Step 1:
(P->Q), (Q->R) => (P->R)

Step 2:
(Q->R), Q => (P->R)
(Q->R) => (P->R), P

Step 3:
(Q->R) => (P->R), P
Q, R => (P->R)
Q => (P->R), Q

Step 4:
Q, R => (P->R)
Q => (P->R), Q
R => (P->R), P
 => (P->R), P, Q

Step 5:
Q => (P->R), Q
R => (P->R), P
 => (P->R), P, Q
Q, R, P => R

Step 6:
R => (P->R), P
 => (P->R), P, Q
Q, R, P => R
Q, P => Q, R

Step 7:
 => (P->R), P, Q
Q, R, P => R
Q, P => Q, R
R, P => P, R

Step 8:
Q, R, P => R
Q, P => Q, R
R, P => P, R
P => P, Q, R

Proved!
```

结合律

```
# python ./test.py --showsteps
Please enter your statement: (P\/(Q\/R))->((P\/Q)\/R)
Deduction starts.

Step 1:
(P\/(Q\/R)) => (P\/Q), R

Step 2:
P => (P\/Q), R
(Q\/R) => (P\/Q), R

Step 3:
P => R, P, Q
(Q\/R) => (P\/Q), R

Step 4:
P => R, P, Q
Q => (P\/Q), R
R => (P\/Q), R

Step 5:
P => R, P, Q
Q => R, P, Q
R => (P\/Q), R

Step 6:
P => R, P, Q
Q => R, P, Q
R => R, P, Q

Proved!
```

## 3.2 非永真式

```
# python ./test.py --showsteps
Please enter your statement: ((P\/Q)/\(P->Q))->(Q->P)
Deduction starts.

Step 1:
(P\/Q), (P->Q) => (Q->P)

Step 2:
(P->Q), P => (Q->P)
(P->Q), Q => (Q->P)

Step 3:
(P->Q), Q => (Q->P)
P, Q => (Q->P)
P => (Q->P), P

Step 4:
P, Q => (Q->P)
P => (Q->P), P
Q, Q => (Q->P)
Q => (Q->P), P

Step 5:
P => (Q->P), P
Q, Q => (Q->P)
Q => (Q->P), P
P, Q, Q => P

Step 6:
Q, Q => (Q->P)
Q => (Q->P), P
P, Q, Q => P
P, Q => P, P

Step 7:
Q => (Q->P), P
P, Q, Q => P
P, Q => P, P
Q, Q, Q => P

Step 8:
P, Q, Q => P
P, Q => P, P
Q, Q, Q => P
Q, Q => P, P

Unproved!
```

```
# python ./test.py --showsteps
Please enter your statement: (((P/\Q)->R)/\((P\/Q)->!R))->(P/\Q/\R)
Deduction starts.

Step 1:
((P/\Q)->R), ((P\/Q)->!R) => (P/\Q/\R)

Step 2:
((P\/Q)->!R), R => (P/\Q/\R)
((P\/Q)->!R) => (P/\Q/\R), (P/\Q)

Step 3:
((P\/Q)->!R) => (P/\Q/\R), (P/\Q)
R, !R => (P/\Q/\R)
R => (P/\Q/\R), (P\/Q)

Step 4:
R, !R => (P/\Q/\R)
R => (P/\Q/\R), (P\/Q)
!R => (P/\Q/\R), (P/\Q)
 => (P/\Q/\R), (P/\Q), (P\/Q)

Step 5:
R => (P/\Q/\R), (P\/Q)
!R => (P/\Q/\R), (P/\Q)
 => (P/\Q/\R), (P/\Q), (P\/Q)
R => (P/\Q/\R), R

Step 6:
!R => (P/\Q/\R), (P/\Q)
 => (P/\Q/\R), (P/\Q), (P\/Q)
R => (P/\Q/\R), R
R => (P\/Q), P
R => (P\/Q), Q
R => (P\/Q), R

Step 7:
 => (P/\Q/\R), (P/\Q), (P\/Q)
R => (P/\Q/\R), R
R => (P\/Q), P
R => (P\/Q), Q
R => (P\/Q), R
 => (P/\Q/\R), (P/\Q), R

Step 8:
R => (P/\Q/\R), R
R => (P\/Q), P
R => (P\/Q), Q
R => (P\/Q), R
 => (P/\Q/\R), (P/\Q), R
 => (P/\Q), (P\/Q), P
 => (P/\Q), (P\/Q), Q
 => (P/\Q), (P\/Q), R

Step 9:
R => (P\/Q), P
R => (P\/Q), Q
R => (P\/Q), R
 => (P/\Q/\R), (P/\Q), R
 => (P/\Q), (P\/Q), P
 => (P/\Q), (P\/Q), Q
 => (P/\Q), (P\/Q), R
R => R, P
R => R, Q
R => R, R

Step 10:
R => P, P, Q
R => (P\/Q), Q
R => (P\/Q), R
 => (P/\Q/\R), (P/\Q), R
 => (P/\Q), (P\/Q), P
 => (P/\Q), (P\/Q), Q
 => (P/\Q), (P\/Q), R
R => R, P
R => R, Q
R => R, R

Step 11:
R => P, P, Q
R => Q, P, Q
R => (P\/Q), R
 => (P/\Q/\R), (P/\Q), R
 => (P/\Q), (P\/Q), P
 => (P/\Q), (P\/Q), Q
 => (P/\Q), (P\/Q), R
R => R, P
R => R, Q
R => R, R

Step 12:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
 => (P/\Q/\R), (P/\Q), R
 => (P/\Q), (P\/Q), P
 => (P/\Q), (P\/Q), Q
 => (P/\Q), (P\/Q), R
R => R, P
R => R, Q
R => R, R

Step 13:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
 => (P/\Q), (P\/Q), P
 => (P/\Q), (P\/Q), Q
 => (P/\Q), (P\/Q), R
R => R, P
R => R, Q
R => R, R
 => (P/\Q), R, P
 => (P/\Q), R, Q
 => (P/\Q), R, R

Step 14:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
 => (P/\Q), (P\/Q), Q
 => (P/\Q), (P\/Q), R
R => R, P
R => R, Q
R => R, R
 => (P/\Q), R, P
 => (P/\Q), R, Q
 => (P/\Q), R, R
 => (P\/Q), P, P
 => (P\/Q), P, Q

Step 15:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
 => (P/\Q), (P\/Q), R
R => R, P
R => R, Q
R => R, R
 => (P/\Q), R, P
 => (P/\Q), R, Q
 => (P/\Q), R, R
 => (P\/Q), P, P
 => (P\/Q), P, Q
 => (P\/Q), Q, P
 => (P\/Q), Q, Q

Step 16:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
R => R, P
R => R, Q
R => R, R
 => (P/\Q), R, P
 => (P/\Q), R, Q
 => (P/\Q), R, R
 => (P\/Q), P, P
 => (P\/Q), P, Q
 => (P\/Q), Q, P
 => (P\/Q), Q, Q
 => (P\/Q), R, P
 => (P\/Q), R, Q

Step 17:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
R => R, P
R => R, Q
R => R, R
 => (P/\Q), R, Q
 => (P/\Q), R, R
 => (P\/Q), P, P
 => (P\/Q), P, Q
 => (P\/Q), Q, P
 => (P\/Q), Q, Q
 => (P\/Q), R, P
 => (P\/Q), R, Q
 => R, P, P
 => R, P, Q

Step 18:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
R => R, P
R => R, Q
R => R, R
 => (P/\Q), R, R
 => (P\/Q), P, P
 => (P\/Q), P, Q
 => (P\/Q), Q, P
 => (P\/Q), Q, Q
 => (P\/Q), R, P
 => (P\/Q), R, Q
 => R, P, P
 => R, P, Q
 => R, Q, P
 => R, Q, Q

Step 19:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
R => R, P
R => R, Q
R => R, R
 => (P\/Q), P, P
 => (P\/Q), P, Q
 => (P\/Q), Q, P
 => (P\/Q), Q, Q
 => (P\/Q), R, P
 => (P\/Q), R, Q
 => R, P, P
 => R, P, Q
 => R, Q, P
 => R, Q, Q
 => R, R, P
 => R, R, Q

Step 20:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
R => R, P
R => R, Q
R => R, R
 => P, P, P, Q
 => (P\/Q), P, Q
 => (P\/Q), Q, P
 => (P\/Q), Q, Q
 => (P\/Q), R, P
 => (P\/Q), R, Q
 => R, P, P
 => R, P, Q
 => R, Q, P
 => R, Q, Q
 => R, R, P
 => R, R, Q

Step 21:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
R => R, P
R => R, Q
R => R, R
 => P, P, P, Q
 => P, Q, P, Q
 => (P\/Q), Q, P
 => (P\/Q), Q, Q
 => (P\/Q), R, P
 => (P\/Q), R, Q
 => R, P, P
 => R, P, Q
 => R, Q, P
 => R, Q, Q
 => R, R, P
 => R, R, Q

Step 22:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
R => R, P
R => R, Q
R => R, R
 => P, P, P, Q
 => P, Q, P, Q
 => Q, P, P, Q
 => (P\/Q), Q, Q
 => (P\/Q), R, P
 => (P\/Q), R, Q
 => R, P, P
 => R, P, Q
 => R, Q, P
 => R, Q, Q
 => R, R, P
 => R, R, Q

Step 23:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
R => R, P
R => R, Q
R => R, R
 => P, P, P, Q
 => P, Q, P, Q
 => Q, P, P, Q
 => Q, Q, P, Q
 => (P\/Q), R, P
 => (P\/Q), R, Q
 => R, P, P
 => R, P, Q
 => R, Q, P
 => R, Q, Q
 => R, R, P
 => R, R, Q

Step 24:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
R => R, P
R => R, Q
R => R, R
 => P, P, P, Q
 => P, Q, P, Q
 => Q, P, P, Q
 => Q, Q, P, Q
 => R, P, P, Q
 => (P\/Q), R, Q
 => R, P, P
 => R, P, Q
 => R, Q, P
 => R, Q, Q
 => R, R, P
 => R, R, Q

Step 25:
R => P, P, Q
R => Q, P, Q
R => R, P, Q
R => R, P
R => R, Q
R => R, R
 => P, P, P, Q
 => P, Q, P, Q
 => Q, P, P, Q
 => Q, Q, P, Q
 => R, P, P, Q
 => R, Q, P, Q
 => R, P, P
 => R, P, Q
 => R, Q, P
 => R, Q, Q
 => R, R, P
 => R, R, Q

Unproved!
```

## 4. 参考

参考课件.
