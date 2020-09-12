const theScript = document.createElement('script');
theScript.innerHTML = `
if (document.getElementsByClassName('page_title')[0].textContent == ' 出房价审批 '){
//出房价审批面积和朝向突出显示,阳台独卫突出
var x = document.getElementsByClassName('el-col el-col-24 el-col-sm-9 el-col-md-9');
for (i = 0;i < x.length; i++){
  if (['朝向','面积'].indexOf(x[i].getElementsByTagName('span')[0].textContent) != -1){
    x[i].getElementsByTagName('span')[1].style.color = '#FF0000'
    x[i].getElementsByTagName('span')[1].style.fontSize = '30px'
    x[i].getElementsByTagName('span')[1].style.fontWeight = 'bold'
  } 
};
//房源卖点突出
var points = x[4].getElementsByClassName("point-item active")
if (points.length != 0) {
  for (i=0;i < points.length;i++) {
    points[i].style.fontSize = '30px';
    points[i].style.fontWeight = 'bold';
    points[i].style.color = '#FF0000';
  }
}
//空置天数超出70天突出
var kongzhi_day = document.getElementsByClassName('lable-value minem7')[4];
if (kongzhi_day.textContent.match("[0-9]+")[0]*1 >= 70) {
  kongzhi_day.style.fontSize = '30px';
  kongzhi_day.style.color = '#FF0000';
  kongzhi_day.style.fontWeight = 'bold';
}
//房屋到期日小于1年突出
var info = document.getElementsByClassName('el-table__row')[0].getElementsByClassName('cell');
if (info.length != 0) {
  nowt = new Date()
  nowt.setFullYear(nowt.getFullYear()+1);
  daoqi_t = new Date (info[2].textContent.replace(/-/g,"/"))
  if (daoqi_t < nowt && info[1].textContent == ' 否 ') {
    info[2].style.color = '#FF0000';
    info[2].style.fontSize = '30px';
    info[2].style.fontWeight = 'bold';
  }
}

//整租4.0突出
var chanpin_type = document.getElementsByClassName('lable-value minem7')[7];
if (chanpin_type.textContent.search('整租') != -1 && chanpin_type.textContent.search('3') != -1) {
  chanpin_type.style.fontSize = '30px';
  chanpin_type.style.color = '#FF0000';
  chanpin_type.style.fontWeight = 'bold';
}
}


if (document.getElementsByClassName('page_title')[0].textContent==' 出房价风控 ') {
//风控面积和朝向突出显示
var y = document.getElementsByClassName('el-col el-col-24 el-col-sm-8 el-col-md-8');
for (i = 0;i < y.length; i++){
  if (['朝向','面积'].indexOf(y[i].getElementsByTagName('span')[0].textContent) != -1){
    y[i].getElementsByTagName('span')[1].style.color = '#FF0000'
    y[i].getElementsByTagName('span')[1].style.fontSize = '30px'
    y[i].getElementsByTagName('span')[1].style.fontWeight = 'bold'
  } 
};
}
`


function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

sleep(5000).then(()=> {
  for (j=1;j<5;j++) {
    document.body.appendChild(theScript);
  }
})

