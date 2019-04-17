### pay attention to the words spell please, or the program will not be executed as expected

0.配置case文件标准采集手机参数（虚拟键、宽高）：
    更多信息请查看/config/sm_collector.ini
        [case_rules]
        定义case采集的样本手机有无navigation_bar
        standard_has_navigation_bar = True
        定义像素密度
        display_size_x = 1080
        display_size_y = 1920
1. 下列支持的选项中，以"V_"开头的量代表可以更改的参数：
      统一标准范式：key(, V_value1, V_value2, V_value...)
2. 每个动作可以选择添加执行之后的等待时间：(, V_wait_several_seconds)，不添加等待时间 默认动作等待间隔0.5s
3. case文件中以'#'开头的行会被解析器忽略
4. 如果需要单独差异化配置case文件的虚拟按键，可以用'display_config'这个参数设置
     （此项参数可缺省，缺省时将当前case以ini配置文件中标准对待）
      "display_config, V_display_size_x, V_display_size_y, V_navigation_bar_height"
      关于虚拟按键高度，在运行sm_collector之后会在手机/sdcard目录下生成phone_info.ini，相关信息会保存至此文件，
      第一次运行脚本后，该文件会被拉取至工程目录下的/output/手机型号_DeviceId_phone_info.ini中
5. 更新配置文件后注意更新代码中的解析模块，否则可能不会执行
6. 所有支持的命令：
      配置case屏幕信息：display_config, V_display_size_x, V_display_size_y, V_navigation_bar_height
      滑动           ：swipe, V_fromX, V_fromY, V_toX, V_toY (, V_wait_several_seconds)
      点击           ：click, V_x, V_y (, V_wait_several_seconds)
      长按           ：hold, V_x, V_y (, V_wait_several_seconds)
      桌面           ：home
      返回           ：back
      等待           ：wait, V_seconds
      特殊模式        ：special_mode
      开启想监控的app  ：start （需要在sm_collector.ini文件中配置启动的Activity）
      停止想监控的app  ：stop
      清除app的数据    : clear_data
      清除手机logcat日志: clear_logcat
      开启监控程序     ：invoke_watcher  （默认是用的SM收集程序 sm_collector.apk）
      开始等待app启动  ：start_command
      停止监控，保存数据：stop_command
      卸载APP         : uninstall   （卸载包名在sm_collector.ini的inspect_object选项中的pkg_name控制）
      安装APP         : install (, V_apk_file_name, V_wait)   （安装apk文件名在sm_collector.ini的inspect_object选项中的to_install_apk控制）
      强制重装APP      : install_r (, V_apk_file_name, V_wait)   （安装apk文件名在sm_collector.ini的inspect_object选项中的to_install_apk控制）
                        install/install_r 虽然操作在adb命令中是阻塞进行，实测发现会有IOError的情况，推荐在安装命令后后睡眠等待
                        install/install_r 后可以直接跟想安装的指定apk名称，差异化每次的安装
      重启手机         ：reboot (, V_wait_several_seconds)
7. examples::
      ### case文件差异化配置（以N5为例：屏幕尺寸1080*1920，导航栏高度144）
      display_config, 1080, 1920, 144
      swipe, 978, 885, 80, 885
      swipe, 978, 885, 80, 885, 5
      click, 905, 1421
      click, 905, 1421, 10
      hold,423,845
      hold,423,845, 8
      home
      back
      wait, 5

      ### special mode 启动的监控case文件示例（launch.txt）：：
      special_mode

      reboot, 60
      stop
      start_command
      wait, 8
      start
      wait, 20
      stop_command
      uninstall
      install_r, example.apk