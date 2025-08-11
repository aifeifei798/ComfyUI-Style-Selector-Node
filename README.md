# ComfyUI Style Selector Node | ComfyUI 风格选择器节点

[English](#english) | [中文](#中文)

A simple but powerful custom node for ComfyUI that allows you to select a predefined style from a dropdown menu and applies your input prompt to a corresponding template. This streamlines the process of experimenting with different styles without manually copying and pasting complex prompt additions.

这是一个为 ComfyUI 设计的简单而强大的自定义节点。它允许您从下拉菜单中选择一个预定义的风格，并将您输入的提示词应用到对应的模板中。这大大简化了风格切换的流程，无需再手动复制和粘贴复杂的提示词。

![node_screenshot](https://github.com/aifeifei798/ComfyUI-Style-Selector-Node/blob/main/comfyui-1-1.png)

![node_screenshot](https://github.com/aifeifei798/ComfyUI-Style-Selector-Node/blob/main/comfyui-1-2.png)

---

## <a name="english"></a>English

### ✨ Features

-   **Dropdown Menu for Styles**: Easily select from a list of predefined art styles.
-   **Dynamic Prompt Formatting**: Automatically inserts your core prompt into the selected style's template.
-   **Separate Outputs**: Provides both positive and negative prompt outputs, fully formatted.
-   **Easily Customizable**: Add, remove, or modify styles by simply editing a Python list in the source file. No complex coding required.

### ⚙️ How to Install

1.  Navigate to your ComfyUI installation directory.
2.  Go to the `ComfyUI/custom_nodes/` folder.
3.  Clone this repository or download the `style_selector_node.py` file into this directory.
    ```bash
    git clone https://github.com/aifeifei798/ComfyUI-Style-Selector-Node.git
    ```
4.  Restart ComfyUI completely.

### 🚀 How to Use

1.  In ComfyUI, double-click or right-click and select "Add Node".
2.  Find the node under the **`Utilities/Text`** category. It will be named **"风格选择器 (Style Selector)"**.
3.  Type your main subject or idea into the `prompt` text box (e.g., `a cat astronaut`).
4.  Select a desired style from the `style_name` dropdown menu.
5.  Connect the `positive_prompt` and `negative_prompt` outputs from this node to the corresponding inputs on your KSampler node (or any other node that accepts prompts).
6.  The node will automatically format the prompts based on your selection. Queue your workflow and see the magic!

### 🔧 How to Customize Styles

You can easily add your own styles!

1.  Open the `style_selector_node.py` file in a text editor.
2.  Locate the `style_list` at the top of the file. It looks like this:

    ```python
    style_list = [
        {"name": "(None)", "prompt": "{prompt}", "negative_prompt": ""},
        {
            "name": "动画4引擎",
            "prompt": "{prompt}, depth of field, faux traditional media...",
            "negative_prompt": "3d, photo, disfigured...",
        },
        # ... more styles
    ]
    ```

3.  To add a new style, simply add a new dictionary to the list with the following format:
    ```python
    {
        "name": "Your Style Name",
        "prompt": "Your positive prompt template, use {prompt} as a placeholder",
        "negative_prompt": "Your negative prompt template"
    }
    ```
    -   `name`: This is the text that will appear in the dropdown menu.
    -   `prompt`: The positive prompt structure. The node will replace `{prompt}` with the text you entered in the node's input box.
    -   `negative_prompt`: The corresponding negative prompt for the style.

4.  Save the file and restart ComfyUI for the changes to take effect.

---

## <a name="中文"></a>中文

### ✨ 功能特性

-   **风格下拉菜单**：从预定义的艺术风格列表中轻松选择。
-   **动态提示词格式化**：自动将您的核心提示词插入到所选风格的模板中。
-   **独立输出**：同时提供格式化完成的正面和负面提示词输出。
-   **易于自定义**：只需编辑源代码文件中的一个 Python 列表，即可添加、删除或修改风格，无需复杂的编程知识。

### ⚙️ 如何安装

1.  导航到您的 ComfyUI 安装目录。
2.  进入 `ComfyUI/custom_nodes/` 文件夹。
3.  克隆本仓库，或直接下载 `style_selector_node.py` 文件到此目录。
    ```bash
    git clone https://github.com/aifeifei798/ComfyUI-Style-Selector-Node.git
    ```
4.  完全重启 ComfyUI。

### 🚀 如何使用

1.  在 ComfyUI 中，双击画布或右键，选择“添加节点 (Add Node)”。
2.  在 **`Utilities/Text`** 分类下找到名为 **“风格选择器 (Style Selector)”** 的节点。
3.  在节点的 `prompt` 文本框中输入您的主要绘画主体或想法（例如 `一只猫宇航员`）。
4.  从 `style_name` 下拉菜单中选择一个您想要的风格。
5.  将此节点的 `positive_prompt` 和 `negative_prompt` 输出连接到您的 KSampler 节点（或任何其他需要提示词的节点）的相应输入端。
6.  节点将根据您的选择自动格式化提示词。点击生成，见证魔法！

### 🔧 如何自定义风格

您可以非常轻松地添加您自己的风格！

1.  用文本编辑器打开 `style_selector_node.py` 文件。
2.  找到文件顶部的 `style_list` 列表。它看起来像这样：

    ```python
    style_list = [
        {"name": "(None)", "prompt": "{prompt}", "negative_prompt": ""},
        {
            "name": "动画4引擎",
            "prompt": "{prompt}, depth of field, faux traditional media...",
            "negative_prompt": "3d, photo, disfigured...",
        },
        # ... 更多风格
    ]
    ```

3.  要添加一个新风格，只需在列表中添加一个遵循以下格式的新字典：
    ```python
    {
        "name": "你的风格名称",
        "prompt": "你的正面提示词模板，使用 {prompt}作为占位符",
        "negative_prompt": "你的负面提示词模板"
    }
    ```
    -   `name`: 将会显示在下拉菜单中的文本。
    -   `prompt`: 正面提示词的结构。节点会自动将 `{prompt}` 替换为您在输入框中输入的文本。
    -   `negative_prompt`: 该风格对应的负面提示词。

4.  保存文件并重启 ComfyUI，您的更改即可生效。
