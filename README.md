# Wang's Algorithm

This is a simple implementation of Wang's Algorithm, which is used to perform automatic proving.

The project include these additional features:
- Automaticly parsing inputs
- Deduction steps visualizing

More features may be added in the future.

A brief introduction of Wang's Algorithm could be found [here](https://courses.cs.washington.edu/courses/cse415/01sp/slides/Prop-resolution/sld009.htm).

# README

- en [English](./README.md)
- zh_cn [简体中文](./readme/README.zh_cn.md)

# Usage

`python ./test.py [--showsteps]`

The flag `--showstps` is to output detailed deduction steps.

Grammar requirements of the initial statement can be found in the next section. If your input statement does not correspond with the grammar rules, the porgram will print an error message and return.

# Grammar

Negative conjunctions: `!`
And conjunctions: `/\`
Or conjunctions: `\/`
Implicit conjunctions: `->`
Biconditional conjunctions: `<->`

Apart from natural constrains of logical statements, these special rules should be followed:

1. An atom-statement is only allowed to be a single capitalized letter.
2. Any spaces or empty statement is forbidden. 
3. The initial statment should be in the form of `A->B`. Here both `A` and `B` are sub-statements. Note that the form of `A->B->C` is forbidden.
4. The left and right parentheses should match one-to-one correspondence. The parentheses should only be used if there exists more than one sub-statement inside them. So the form of `(A)` is forbidden.
5. More than two statements connected by either `\/`s or `/\`s is allowed. Any other situations should specify the priority of calculation in the form of parentheses. For example, `(A/\B/\C)` and `(A/\(B\/C))` are allowed, but `(A\/B/\C)` and `(A->B\/C)` are forbidden.

# Limitations/Future improvements

This is just a simple demo developed within 6 hours, so there may be some bugs or edge conditions that I haven't thought of.

And below is some of the drawbacks I can think of that could possibly be refined in the future, as long as I have spare time.

1. For-loops are frequently used in this project, so it might be better to replace some of the linear search with more efficient data structures.
2. For simplicity of the development, I did not operate in-place transition in the list structure, but just delete the original element and add new one in the back, thus resulting in some chaos of the order of the statements in the deduction steps showed (still correct though). And deduction basis could be added too.
3. Also for simplicity, I did not output the specific error message, but only print a general one when detects grammar mistakes. It might be more user-friendly if the program can output the specific type of error or even the position of the error.
4. I did not deal with possible duplicate statements.
5. Try to leave some comments in the code.
