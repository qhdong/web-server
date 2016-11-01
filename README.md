# A simple web server written by python3

这是500 lines中的一个小项目，具体地址在[这里](http://aosabook.org/en/500L/a-simple-web-server.html)

原版是使用`python2`编码的，我使用`python3`完成，通过此项目，能够了解作为一个web服务程序的基本原理，同时也掌握一些设计方法：

- 将类设计为一系列服务的集合，他们自身并不做出决策，而是提供服务
- 可扩展性，通过封装和解偶，屏蔽底层细节，遵循开闭原则，对扩展开放，对修改封闭