function dateFtt(fmt, date) { //author: meizz 
	var o = {
		"M+": date.getMonth() + 1, //月份 
		"d+": date.getDate(), //日 
		"h+": date.getHours(), //小时 
		"m+": date.getMinutes(), //分 
		"s+": date.getSeconds(), //秒 
		"q+": Math.floor((date.getMonth() + 3) / 3), //季度 
		"S": date.getMilliseconds() //毫秒 
	};
	if (/(y+)/.test(fmt))
		fmt = fmt.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length));
	for (var k in o)
		if (new RegExp("(" + k + ")").test(fmt))
			fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
	return fmt;
}

function newDates() {
	const now = new Date();  // 获取当前时间对象
	const year = now.getFullYear();
	const month = String(now.getMonth() + 1).padStart(2, '0');
	const day = String(now.getDate()).padStart(2, '0');
	const hours = String(now.getHours()).padStart(2, '0');
	const minutes = String(now.getMinutes()).padStart(2, '0');
	const seconds = String(now.getSeconds()).padStart(2, '0');
	const milliseconds = String(now.getMilliseconds()).padStart(3, '0');
	const timezoneOffset = -now.getTimezoneOffset();
	const timezoneOffsetHours = String( Math.floor(timezoneOffset / 60)).padStart(2, '0');
	const timezoneOffsetMinutes = String(timezoneOffset % 60).padStart(2, '0');
	const timezoneString = timezoneOffset >= 0 ? `+${timezoneOffsetHours}:${timezoneOffsetMinutes}` : `-${timezoneOffsetHours}:${timezoneOffsetMinutes}`;
	const dateString = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}.${milliseconds}${timezoneString}`;
	return dateString
}

export default {
	// 格式化日期时间
	rTime(date) {
		return dateFtt('yyyy-MM-dd hh:mm:ss', new Date(date))
	},
	// 格式化日期
	rDate(date) {
		return dateFtt('yyyy-MM-dd', new Date(date))
	},

	//生成当前最新的时间格式为 yyyy-MM-dd hh:mm:ss
	newTime() {
		return newDates()
	}
}
