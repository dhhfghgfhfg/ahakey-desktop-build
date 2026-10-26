# AhaKey macOS 社区功能兼容构建

构建日期：2026-10-26。面向 macOS 12.7.6、Intel x86_64。

## 安装

1. 完全退出旧版 AhaKey Studio，避免两个版本同时占用键盘。
2. 打开 DMG，将 AhaKey Studio Community.app 拖到 Applications。
3. 本包为临时签名、未公证的自行构建版本。如 macOS 阻止首次启动，请在 Finder 中右键应用并选择“打开”，或按“系统偏好设置 → 安全性与隐私”中的提示允许打开。
4. 按客户端提示授予蓝牙权限；使用语音功能时另行授予麦克风、语音识别及辅助功能权限。

也可解压 ZIP，将完整的 .app 放入 Applications。ZIP 保留了 macOS 应用包权限和资源信息。

## 版本与功能

基于 AhakeyAI/desktop 公开仓库 main 的 0ddab17fc8128d4090a5f1963354be666771f6f3，包含 VibeBar、键盘配置、Agent 与现有语音功能；版本标识沿用源码的 0.2.3，属于 main 后续提交的兼容构建，并非官方 v0.2.3 发布包。

官网社区版下载包名为 ocean-light-compat，未标注源码提交。本包未能确认与该定制包完全相同的界面或二进制来源，以公开社区功能源码为准。

兼容改动：主程序与 VibeBar 的最低系统改为 12.0；DynamicNotchKit 1.0.0 使用保留 MIT 许可的本地兼容副本；macOS 12 使用旧菜单栏与动画、布局观察实现。

## 验证范围

构建流程执行应用/Agent/共享模块和 VibeBar 测试，核查主程序、Agent 及 Intel 烧录工具的 Mach-O 最低系统版本，校验临时签名与 DMG 完整性。详细结果见 build-info.json、macos12-binary-audit.json 与构建日志。

构建机器为 GitHub macOS 15 runner，尚未在真实 macOS 12.7.6 上验证启动、蓝牙、VibeBar 或语音；需要在目标机器完成实机复测。此包不支持 Apple Silicon 原生运行。

SHA256SUMS 提供 DMG 和 ZIP 的校验值。源码变更与 DynamicNotchKit 来源记录位于对应构建分支的 build-support/macos12 和 vendor/DynamicNotchKit。
