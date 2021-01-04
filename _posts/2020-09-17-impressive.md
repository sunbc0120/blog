---
toc: false
layout: post
badges: true
comments: false
show_image: true
hide: false
description: Get up to speed with Markdown typing and formatting.
categories: [markdown]
title: How To Be More Impressive
---

## Practise Markdown Math typing and formatting by reproducing:

{% twitter https://twitter.com/phant0msp1k3/status/1271060499338342407 %}


Suppose we want to publish something that is as simple as

> To have numbered equation, type:
> ```latex
> $$1+1=2\tag{1}$$
> ```
> Pay attention to the `\tag{1}`. Unlike _LaTex_, you have to manage numbering and reference yourself in _Markdown_.

$$1+1=2\tag{1}$$

This is not very impressive. If we want our article to be accepted by _IEEE_ reviewers, we have to be more abstract. So, we could complicate the left hand side of the expression by using
> To have text in between equations in the same line, type:
> ```latex
> $$\ln(e) = 1 \text{  and  } \sin^2x + \cos^2 x = 1$$
> ```
> Pay attention to the `space` before and after the `and` in the `{}`.

$$\ln(e) = 1 \text{  and  } \sin^2x + \cos^2 x = 1$$

and the right hand side can be stated as
> This one is similar to _LaTex_, type:
> ```latex
> $$2=\sum_{n=1}^\infty\frac{1}{2^n}$$
> ```
 
$$2=\sum_{n=1}^\infty\frac{1}{2^n}$$

Therefore, Equation (1) can be expressed more scientificially as:
> Type
> ```latex
> $$\ln(e) + (\sin^2x + \cos^2 x) = \sum_{n=1}^\infty\frac{1}{2^n} \tag{2}$$ 
> ```
> Pay attention to the `\tag{2}`. 

$$\ln(e) + (\sin^2x + \cos^2 x) = \sum_{n=1}^\infty\frac{1}{2^n} \tag{2}$$

which is far more impressive. However, we should not stop here. The expression can be further complicated by using

> Type
> ```latex
> $$e = \lim_{z\rightarrow\infty}(1+\frac{1}{z})^z \text{ and } 1=\cosh(y)\sqrt{1-\tanh^2y}$$
> ```
> Pay attention to the `space` before and after `and`, again.

$$e = \lim_{z\rightarrow\infty}(1+\frac{1}{z})^z \text{ and } 1=\cosh(y)\sqrt{1-\tanh^2y}$$

Equation (2) may therefore be written as
> This equation is "impressive",
> ```latex
> $$\ln\left[\lim_{z\rightarrow\infty}(1+\frac{1}{z})^z\right] + \left(\sin^2x + \cos^2 x\right) = \sum_{n=1}^\infty \frac{\cosh(y)\sqrt{1-\tanh^2y}}{2^n} \tag{3}$$
> ```
> Pay attention to the first pair of brackets `[]`: it comes with `\left[` and `\right]`. Without `\left` and `\right`, the bracket will be smaller or shorter, which won't contain the full height of $\lim_{z\rightarrow\infty}(1+\frac{1}{z})^z$.

$$\ln\left[\lim_{z\rightarrow\infty}(1+\frac{1}{z})^z\right] + \left(\sin^2x + \cos^2 x\right) = \sum_{n=1}^\infty \frac{\cosh(y)\sqrt{1-\tanh^2y}}{2^n} \tag{3}$$

**Note**: Other methods of a similar nature could also be used to enhance our prestige, once we grasp the underlying pringciples.
