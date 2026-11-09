# ❄️ 雾凇中日混输方案 (Rime-Ice-Mix)

> [!NOTE]
> **作者说明**：  
> 本输入法基本上都是基于 AI 制作的，README 也是 AI 写的，比较花哨，ai部署的时候让总结一下就好了。主要功能就是中文日文英文混合输入，有需要自定义的功能也可以让 AI 帮你改一下。  
> 另外就是拼音反查功能有点 bug，主要是查询单个汉字的时候会不准，然后提示读音好像也有点问题，其余基本上没什么问题了。Rime 也是开源输入法，用 AI 帮你自定义就很方便，比如我就让 DIY 成和 macOS 原生输入法 UI 基本上一样的样子，おすすめです！

<p align="center">
  <img src="https://img.shields.io/badge/Rime-鼠须管%20Squirrel-34ad9b?style=flat-square&logo=apple" alt="Rime Squirrel">
  <img src="https://img.shields.io/badge/Base-雾凇拼音%20rime--ice-blue?style=flat-square" alt="rime-ice">
  <img src="https://img.shields.io/badge/Japanese-Mozc%20%2B%20JMdict%20(40W%2B)-red?style=flat-square" alt="Mozc">
  <img src="https://img.shields.io/badge/License-GPL--3.0-orange?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome">
</p>

> 基于广受好评的开源输入法配置 **[雾凇拼音 (rime-ice)](https://github.com/iDvel/rime-ice)** 构建，深度融合 **Mozc + JMdict（40万+ entries）** 现代日语大词库。  
> 独创解决普通中日混输方案中**单 n 拨音污染中文**、**片假名长音输入冲突**、**繁简转换篡改日文汉字**三大核心痛点，并原生集成**拼音反查日文新字体（带读音提示）** 与 **macOS 苹果系统文本替换秒级热同步**。

---

## 💡 为什么需要这个方案？（解决的痛点）

市面上常见的中日混输方案虽然能够“中日混打”，但在日常高频输入中往往存在令人抓狂的体验问题：

| 常见痛点 | 传统混输方案的困扰 | ❄️ Rime-Ice-Mix 的解决方案 |
| :--- | :--- | :--- |
| **拨音单 `n` 污染中文** | 打 `pan`（盘）、`san`（三）、`kantan`（侃谈）时，单 `n` 会疯狂冒出日语假名 `パン`、`さん`，严重干扰中文打字。 | **严格 `nn` 约束**：重构并清洗全部 40 万条日语词典，拨音 `ん/ン` **必须且只能通过 `nn` 触发**。输入 `pan` 100% 是中文，输入 `pann` 才是 `パン`。 |
| **片假名长音「ー」冲突** | Rime 默认把键盘 `-` 键占用为翻页键（`Page_Up`），导致连打 `ko-hi-`（咖啡）、`ra-menn`（拉面）时按键被截断，根本打不出长音。 | **原生级 `-` 长音支持**：将翻页键移交给更舒适通用的逗号 `,` 和句号 `.`，彻底释放 `-` 键。单按 `-` 秒出 `1. ー`，词中输入 `ko-hi-` 直出 `コーヒー`。 |
| **繁简转换误篡改日文** | 开启输入法简繁切换后，日文假名或和制汉字经常被 OpenCC 强行繁体化或简体化。 | **繁简逃逸保护**：精准配置 `excluded_types: [ table ]`，日语词库产生的内容免受任何 OpenCC 规则篡改。 |
| **不会日语读音无法输入** | 遇到不知道日文读音的汉字词汇时，只能切回中文输入法打出来再切回来。 | **拼音反查日文新字体**：按 `<kbd>(即1左边那个键)` 引导键 + 拼音直接反查！且自主构建了 40 万条日文新字体映射库，杜绝出传统繁体字（如 `寫真`），精准输出日文新字体（`写真`）并标注罗马字注音 `〔shashinn〕`。 |
| **快捷短语配置繁琐** | 每次要添加自定义短语（电话、地址等），都必须手动修改文本文件再重新部署。 | **与苹果设置秒级实时热同步**：直接联动 macOS 本地数据库，在系统设置或 iPhone 添加文本替换，后台自动秒级热重载，零感知生效！ |

---

## ✨ 核心特性一览

### 1. 中日自然混输（`nn` 严格隔离）
* **日常中文零干扰**：拼音输入体验与原生雾凇拼音完全一致。
* **拨音精准匹配**：
  * `sann` $\rightarrow$ `さん` / `三`（输入 `san` 则是纯中文 `三` / `散` / `伞`）
  * `pann` $\rightarrow$ `パン`（输入 `pan` 则是纯中文 `盘` / `判`）
  * `nihonn` $\rightarrow$ `日本` / `にほん`
  * `renntou` / `rennyou` $\rightarrow$ `連用`
  * `shinnya` $\rightarrow$ `深夜`
  * `kinnyoubi` $\rightarrow$ `金曜日`
* **假名置顶**：输入 `nn` 绝对置顶 `1. ん`、`2. ン`。

### 2. 原生片假名长音「ー」连打
* 单击 `-` 键直接输出 **`1. ー`**
* 词中连打片假名长音毫无阻碍：
  * `ko-hi-` $\rightarrow$ `コーヒー`
  * `ra-menn` $\rightarrow$ `ラーメン`
  * `su-pa-` $\rightarrow$ `スーパー`
  * `me-ru` $\rightarrow$ `メール`
  * `ge-mu` $\rightarrow$ `ゲーム`
  * `bi-ru` $\rightarrow$ `ビール`
  * `pa-ti-` $\rightarrow$ `パーティー`

### 3. 反查神器：拼音反查日文新字体（含注音提示）
按下反引号 <kbd>`</kbd> + 汉语拼音，即可反查日本汉字及现代日文写法，候选项右侧自带该汉字/词汇在日语词库中的罗马字注音：

| 反查输入 | 候选输出与读音提示 | 汉字形态说明 |
| :--- | :--- | :--- |
| **`` `xiezhen ``** / **`` `zhaopian ``** | `1. 写真 〔shashinn〕` | 自动匹配日文新字体（非康熙繁体 `寫真`） |
| **`` `wei ``** / **`` `yinwei ``** | `1. 為 〔tame/i〕` | 自动匹配日文常用体（非繁体 `爲`） |
| **`` `yinghua ``** | `1. 桜 〔sakura〕` | 自动匹配日文新字体（非繁体 `櫻`） |
| **`` `guang ``** | `1. 広 〔hiro/kou〕` | 自动匹配日文新字体（非繁体 `廣`） |
| **`` `qi ``** | `1. 気 〔ki〕` | 自动匹配日文新字体（非繁体 `氣`） |
| **`` `lianyong ``** | `1. 連用 〔rennyou〕` | 精准匹配日语语法词「連用」 |
| **`` `xuexiao ``** | `1. 学校 〔gakkou〕` | 自动匹配日文「学校」（非繁体 `學校`） |
| **`` `yueding ``** | `1. 約束 〔yakusoku〕` | 自动对应日文「約束」 |

### 4. 与苹果系统设置「文本替换」实时热同步 (macOS Exclusive)
* 深度打通 macOS 原生文本替换数据库（`~/Library/KeyboardServices/TextReplacements.db`）。
* **自动化后台守护（LaunchAgent）**：
  * 只要你在 Mac「系统设置 $\rightarrow$ 键盘 $\rightarrow$ 文本替换」或 iPhone / iPad（开启 iCloud 自动同步）中新增、修改或删除短语；
  * 后台监听器会在秒级内自动将其提取并同步至 `custom_phrase.txt`；
  * 同时自动触发鼠须管（Squirrel）内存热重载，**完全无需手动点击重新部署，新短语立即可用**！

### 5. 纯净三方案设计
按下 <kbd>Control</kbd> + <kbd>`</kbd>（或 <kbd>F4</kbd>）呼出的方案选单保持绝对纯净：
```text
「方案选单」
1. 雾凇中日混输 (rime_ice_mix)
2. 雾凇拼音 (rime_ice)
3. 雾凇繁体 (rime_ice_tw)
```
* **简繁独立隔离**：切到「雾凇繁体」输入繁体，切回混输或纯拼音必定秒回简体，彻底杜绝状态串扰。
* **去除冗余选项**：彻底剔除底部的二级折叠菜单；
* **保留中英气泡**：单按 <kbd>Shift</kbd> 时精准保留屏幕中间的「中 / A」浮动切换提示。

### 6. 继承雾凇拼音全套强大扩展
* **时间日期星期**：输入 `rq`（日期）、`sj`（时间）、`xq`（星期）、`dt`（完整时间戳）、`nl`（农历）。
* **大写金额与数字**：输入 `R12345.67` $\rightarrow$ `壹万贰仟叁佰肆拾伍元陆角柒分`。
* **简易计算器**：输入 `cC128*3+5` $\rightarrow$ `389`。
* **以词定字**：候选状态下输入 <kbd>[</kbd> 选取首字，输入 <kbd>]</kbd> 选取尾字。
* **错音错字纠错**：如输入 `geiyu` 提示 `给予 [jǐ yǔ]`。

---

## 📦 安装与配置指南

### 前置要求
* 操作系统：**macOS**
* 输入法框架：**[鼠须管 (Squirrel)](https://github.com/rime/squirrel/releases)**（建议版本 $\ge 0.16.0$）

### 1. 备份现有配置
在终端中执行命令备份当前的 Rime 配置：
```bash
cp -r ~/Library/Rime ~/Library/Rime_backup_$(date +%Y%m%d)
```

### 2. 克隆本仓库到 Rime 配置目录
```bash
# 复制或克隆本仓库到 ~/Library/Rime
git clone https://github.com/aysy2333/Rime-Config.git ~/Library/Rime
```

### 3. 配置自定义短语
仓库默认提供了模板文件 `custom_phrase.example.txt`：
```bash
cd ~/Library/Rime
cp custom_phrase.example.txt custom_phrase.txt
```
*(注：`custom_phrase.txt` 中保留了 `ん`、`ン`、`ー` 的核心置顶规则，请勿删除)*

### 4. 启用与苹果系统文本替换自动同步（推荐）
如果你希望输入法自动同步 macOS 系统设置 / iPhone iCloud 中的文本替换短语：
```bash
cd ~/Library/Rime
# 1. 立即执行一次初次全量同步
python3 sync_apple_text_replacements.py --force

# 2. 注册并启动 macOS 后台自动监听守护服务
launchctl load ~/Library/LaunchAgents/com.rime.sync_text_replacements.plist 2>/dev/null || true
```
以后只需在 Mac **「系统设置 $\rightarrow$ 键盘 $\rightarrow$ 文本替换」** 里维护短语，输入法后台将自动检测并秒级热重载生效！

### 5. 重新部署
点击 Mac 顶部菜单栏的输入法图标，选择 **「重新部署」**（或按快捷键 <kbd>Control</kbd> + <kbd>Option</kbd> + <kbd>\</kbd>）。等待部署完成的提示弹出即可！

---

## ⌨️ 常用按键与操作速查

| 操作 | 快捷键 / 触发方式 | 说明 |
| :--- | :--- | :--- |
| **候选翻页** | 逗号 <kbd>,</kbd> 上翻 / 句号 <kbd>.</kbd> 下翻 | 释放了 `-` 键给日语长音符，同时兼容 <kbd>=</kbd> 和 <kbd>Tab</kbd> |
| **拼音反查日语** | <kbd>`</kbd>（反引号）+ 拼音 | 如打 `` `lianyong `` 出 `連用` |
| **方案选单** | <kbd>Control</kbd> + <kbd>`</kbd> 或 <kbd>F4</kbd> | 切换混输、简体、繁体方案 |
| **中英切换** | 单击 <kbd>Shift</kbd> | 屏幕中间显示「中 / A」气泡 |
| **以词定字** | 候选中按 <kbd>[</kbd> 或 <kbd>]</kbd> | 分别提取第一个字与最后一个字 |
| **长音符输入** | 单击 <kbd>-</kbd> 键 | 快速上屏 `ー` |

---

## 🔒 隐私与安全性保障

* 用户的个人敏感信息（如手机号、私人邮箱、家庭住址、身份证等）通常记录在 `custom_phrase.txt` 中。
* 本仓库已经在 `.gitignore` 中严格将 `custom_phrase.txt`、`.apple_text_replacements.hash`、日志缓存等私密文件全面排除，**不会将你的个人隐私信息推送提交至公开的 Git 仓库**。

---

## 🙏 鸣谢与致敬

本方案站在巨人的肩膀上完成，由衷感谢以下卓越的开源项目及社区贡献者：

* **[rime-ice (雾凇拼音)](https://github.com/iDvel/rime-ice)**：提供现代、纯净且高质量的中文词库及丰富的 Lua 脚本扩展体系。
* **[Rime / 鼠须管 (Squirrel)](https://github.com/rime/squirrel)**：强大神级跨平台输入法算法框架。
* **[Mozc](https://github.com/google/mozc) & [JMdict](https://www.edrdg.org/jmdict/j_jmdict.html)**：提供庞大精准的开源日语现代词汇与假名映射支持。
* **[OpenCC](https://github.com/BYVoid/OpenCC)**：开箱即用的优质中文汉字转换架构。

---

## 📄 开源许可证

本项目基于 [GPL-3.0 许可证](LICENSE) 开源。
