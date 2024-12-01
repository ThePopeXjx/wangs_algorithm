# 王浩算法

这是一个王浩算法的简单实现，用于自动证明.

本项目包含以下特性：
- 自动输入解析
- 归结步骤可视化

更多特性可能在未来添加.

[王浩算法的简单介绍](https://courses.cs.washington.edu/courses/cse415/01sp/slides/Prop-resolution/sld009.htm).

# README

- 英语 [English](./README.md)
- 简体中文 [简体中文](./readme/README.zh_cn.md)

# 用法

`python ./test.py [--showsteps]`

参数`--showstps`用于输出详细推理步骤.

初始命题的语法要求可以在下一章节找到. 如果你的输入不符合初始要求，程序会打印错误信息并退出.

# 语法

否定联结词: `!`
合取联结词: `/\`
析取联结词: `\/`
蕴含联结词: `->`
双蕴含联结词: `<->`

除了命题的自然要求，需要遵守另一些特殊规则:

1. 每个原子命题都只能被表示为大写字母.
2. 不允许出现空格或空命题. 
3. 初始命题的形式为`A->B`. 这里`A`和`B`都是子命题. 注意`A->B->C`的形式是不允许的.
4. 左右括号应一一对应. 只有在其内部有大于等于两个子命题时，括号才可以使用. 因此`(A)`的形式是不允许的.
5. 大于两个被要么全为`\/`，要么全为`/\`所连接的命题是允许的. 其他情况下必须由括号指明运算优先级. 例如, `(A/\B/\C)`和`(A/\(B\/C))`是允许的, 但是`(A\/B/\C)`和`(A->B\/C)`是不允许的.

# 局限/未来改进

这只是一个在6小时内开发的简单demo, 因此可能有一些我没有考虑到的潜在bug和边缘情况.

以下是一些我可以想到的有待改进的缺陷，当然只要有时间的话.

1. 遍历在项目中被大量使用，可能换成一些高效率的数据结构更好.
2. 为了开发便利，我没有对list做原地操作，而是简单地把原元素删除，把新元素加在最后，因此推理步骤中的命题顺序看起来有些奇怪（虽然它们仍然是正确的）. 同时也可以考虑添加推理依据.
3. 同样是为了开发便利，我没有输出具体的格式错误信息，只是告诉你有地方错了. 如果能输出错误的类型甚至错误的位置，可能对使用者更友好.
4. 未对可能的命题重复进行去重.
5. 可以在代码里写点注释.