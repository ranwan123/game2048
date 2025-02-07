[app]

# 游戏标题和包名
title = 2048 Game
package.name = game2048
package.domain = org.test

# 源代码文件
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# 游戏版本
version = 1.0

# 需要的依赖
requirements = python3,pygame,kivy

# Android 特定设置
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 23b
android.sdk = 31
android.accept_sdk_license = True

# 方向设置
orientation = portrait

# 图标设置
#icon.filename = %(source.dir)s/icon.png

# 不需要的权限
android.permissions = INTERNET

# 应用描述
description = A 2048 puzzle game

# 作者信息
author = Your Name
author_email = your.email@example.com 