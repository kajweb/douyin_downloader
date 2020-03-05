const { remote } = require("electron");
const { BrowserWindow } = remote;
var http=require("http");
var https=require("https");
var cheerio = require('cheerio')

mbUA = "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3"

// 文本框
var inputUrl = document.getElementById('text-url')
// 下载按钮
var btDown = document.getElementById('bt-down')
// 警告
var divTips = document.getElementById('div-tips')
var divTipsText = document.getElementById('div-tips-text')
var divTipsClose = document.getElementById('div-tips-close')

// 设置软件标题
thisWindow = remote.getCurrentWindow()
thisWindow.setTitle("抖音视频下载v1.0.0  -  by:kajweb")

// 点击下载按钮
btDown.addEventListener('click', (e) => {
	let inputUrlValue = inputUrl.value
	if( inputUrlValue == "OpenDevTools" ){
		thisWindow.webContents.openDevTools({mode:'detach'})
		inputUrl.value = ""
		divTipsText.innerHTML = "已打开控制台";
		divTips.style.display = "block"
		return false;
	}
	if(inputUrlValue.substr(0,7).toLowerCase() == "http://" || inputUrlValue.substr(0,8).toLowerCase() == "https://"){
	    url = inputUrlValue;
	}else{
	    url = "https://" + inputUrlValue;
	}
	divTipsText.innerHTML = "正在打开链接";
	getHttp(url).then((e)=>{
		$ = cheerio.load(e)
		src = $('#theVideo').attr('src')
		if( src ){
			srcWithMask = src.replace("\/playwm\/","\/play\/")
			openVideo(srcWithMask)
			divTips.style.display = "none"
		}else{
			throw("下载失败，请检查URL")
		}
	}).catch((err)=>{
		console.log("err")
		divTipsText.innerHTML = err;
		divTips.style.display = "block"
	})
})


inputUrl.addEventListener('keydown', (e) => {
	divTips.style.display = "none"
	if( e.keyCode == 13 ){
		btDown.click()
	}
})


divTipsClose.addEventListener('click', (e) => {
	divTips.style.display = "none"
})


// 打开视频
function openVideo(url){
	let downlaoder = new BrowserWindow({
		width: 480,
		height: 853,
		show: false
	})
	downlaoder.once('ready-to-show',()=>{
		downlaoder.show()
		downlaoder.setTitle("请点击视频右下角进行下载")
	})
	downlaoder.loadURL( url, {userAgent: mbUA} )
}

// 获取链接
function getHttp(originUrl){
    return new Promise((resolve, reject) => {
		try{
			url = new URL(originUrl)
			var xmlHttp = (url.protocol == 'https:' ? https : http);
		}catch(err){
			consloe.log("eraasd")
			reject("URL错误，请检查URL")
		}
        let options={
            headers: {
                'User-Agent': mbUA
            }
        }
		req = xmlHttp.get( url.href, options ,function(res){
			console.log(res.headers)
			const { statusCode } = res;
			if (statusCode == 301 || statusCode == 302) {
				resolve(getHttp(res.headers['location']))
			}
		    var str="";
		    // res.setEncoding('utf8');
		    res.on("data",function(chunk){
		        str += chunk
		    })
		    res.on("end",function(){
		        xml = str.toString()
		        resolve(xml)
		    })
		})
		req.on("error",function(err){
		    reject(`请求失败，错误原因：${err.message}`);
		})
    })
}