# File Structure Creator
This is a small utility tool that creates directory structures based on textual descriptions.
It can generate project structures such as the following example:

Example Structure Generation
Given a description file, it can create:

这是一个根据文件描述创建目录结构的小工具。
可以建立如下结构的项目结构在“file.txt”：
│
├── index.html
├── main.js
├── assets/
│   ├── css/
│   ├── images/
│   └── js/
└── components/
    ├── Login.vue
    └── SystemManagement.vue

pip install file_structure_creator
create-structure file.txt
pip show file_structure_creator
## 安装

```bash
pip install file_structure_creator