while true
do
	select name in "部署项目" "重启项目" "暂停项目" "删除项目" "退出菜单"
	do
		case $name in
			"部署项目")
				deploy
				break
				;;
			"重启项目")
				restart
				break
				;;
			"暂停项目")
				close
				break
				;;
			"删除项目")
				delete
				break
				;;
			"退出菜单")
				echo "退出菜单"
				exit 0
				;;
			*)
				echo "无效选项"
				;;
		esac
	done
done
