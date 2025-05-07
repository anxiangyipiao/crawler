import json
import requests
import random
import os





X_YP_Access_Token = "a36a90f6-d119-4b50-970f-30894a2f39fa"



contents = '''
<body>
<div class="header">
    <nav class="navbar navbar-default" role="navigation"><div class="container">
            <div class="navbar-header">
                 <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1"> <span class="sr-only">Toggle navigation</span><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></button>
                 <a class="navbar-brand" href="../index.htm"></a>
            </div>
            <div class="nav navbar-right top-right">
                  <a href="#" onclick="this.style.behavior='url(#default#homepage)';this.setHomePage(location);">设为首页</a>|
                <a href="javascript:window.external.AddFavorite(location.href,document.title)">加入收藏</a>| 
                  <a href="../xxgl/ywjs.htm">English</a>|
                   <div style="padding-top:10px;margin:0 auto;width:300px;text-align:center;padding-left:30px;padding-bottom: 20px;">
                   <div><script type="text/javascript">
    function _nl_ys_check(){
        
        var keyword = document.getElementById('showkeycode202903').value;
        if(keyword==null||keyword==""){
            alert("请输入你要检索的内容！");
            return false;
        }
        if(window.toFF==1)
        {
            document.getElementById("lucenenewssearchkey202903").value = Simplized(keyword );
        }else
        {
            document.getElementById("lucenenewssearchkey202903").value = keyword;            
        }
        var  base64 = new Base64();
        document.getElementById("lucenenewssearchkey202903").value = base64.encode(document.getElementById("lucenenewssearchkey202903").value);
        new VsbFormFunc().disableAutoEnable(document.getElementById("showkeycode202903"));
        return true;
    } 
</script>
<form action="../search.jsp?wbtreeid=1039" method="post" id="au0a" name="au0a" onsubmit="return _nl_ys_check()" style="display: inline">
 <input type="hidden" id="lucenenewssearchkey202903" name="lucenenewssearchkey" value=""><input type="hidden" id="_lucenesearchtype202903" name="_lucenesearchtype" value="1"><input type="hidden" id="searchScope202903" name="searchScope" value="0">
 <span style="font-size: 9pt;    float: left;    line-height: 25px;">站内搜索：</span><input name="showkeycode" id="showkeycode202903" style="  float: left; height: 25px;    display: block;    width: 122px;    padding: 6px 12px;    font-size: 14px;    line-height: 1.42857143;    color: #555;    border-radius: 20px;    background-color: #fff;    border: 0;    box-shadow: none;">
 <input type="submit" align="absmiddle" value="查询" style="width: 60px; float: left;line-height: 25px !important;    -webkit-appearance: button;    cursor: pointer;    background-color: transparent;    border: 0px;    color: inherit;    font: inherit;    margin: 0;">
    <div style="clear:both;"></div>

</form><script language="javascript" src="/system/resource/js/base64.js"></script><script language="javascript" src="/system/resource/js/formfunc.js"></script>
</div>
                   </div>
            </div>
            
     
              <div class="wrapper">
                <div class="header">
                    <div class="nav">
                        <ul class="menu">
                            <li class="list-menu current">
                                <a href="../index.htm"><i class="fa fa-home"></i> 网站首页</a></li>
                            <li class="list-menu">
                                <a class="bind_menu_a" href="http://www.lntdxy.com/xxgl/xxjj.htm" data-layerid="layer1"><i class="fa fa-building-o"></i> 学校概览</a>
                            </li>
                            <li class="list-menu">
                                <a class="bind_menu_a" href="http://www.lntdxy.com/jgsz/jxjg.htm" data-layerid="layer2"><i class="fa fa-sitemap"></i> 机构设置</a>
                            </li>
                            <li class="list-menu">
                                <a class="bind_menu_a" href="http://www.lntdxy.com/dhlm/jxky.htm" data-layerid="layer3"><i class="fa fa-book"></i> 教学科研</a>
                            </li>
                            <li class="list-menu">
                                <a class="bind_menu_a" href="http://www.lntdxy.com/dhlm/zsjy.htm" data-layerid="layer4"><i class="fa fa-users"></i> 招生就业</a>
                            </li>
                            <li class="list-menu">
                                <a class="bind_menu_a" href="http://www.lntdxy.com/dhlm/xqhz.htm" data-layerid="layer5"><i class="fa fa-handshake-o"></i> 校企合作</a>
                            </li>
                            <li class="list-menu">
                                <a class="bind_menu_a" href="http://www.lntdxy.com/dhlm/xgzx.htm" data-layerid="layer6"><i class="fa fa-graduation-cap"></i> 学工在线</a>
                            </li>
                            <li class="list-menu">
                                <a class="bind_menu_a" href="http://www.lntdxy.com/xxgk/xxgkzn.htm" data-layerid="layer7"><i class="fa fa-bullhorn"></i> 信息公开</a>
                            </li>
                        </ul>
                        <div class="sub_menu bind_menu_a" id="layer1" data-layerid="layer1" style="display: none;">
                            <i></i>
                            <div class="sub_area clearfix">
                                <div class="sub_img">
                                    <a title="" alt="" href="#"><img src="../images/menu1.jpg" class="img-responsive"></a>
                                </div>
                                <div class="sub_content">
                                        <h4>学校概览</h4>
                                        <p>学校始建于1948年，2008年升格为高职院，现为首批辽宁省职业教育改革发展示范学校。现有全日制在校生7514人；开设23个专业；已建成国家级示范专业点1个，国家级ICT行业创新基地1个，省级示范专业7个，省高水平特色专群2个，形成了以轨道交通专业为主体，以装备制造和信息类专业为支撑的专业办学格局。</p>
                                        <div class="btn btn-info"><a href="../xxgl/xxjj.htm" target="">详细介绍</a></div>
                                </div>
                                <div class="sub_btn">
                                    <div class="btn btn-primary"><a href="../xxgl/xxjj.htm" target="">学校简介</a></div>
                                    <div class="btn btn-primary"><a href="../xxgl/xxzc.htm" target="">学校章程</a></div>
                                    <div class="btn btn-primary"><a href="../xxgl/xrld.htm" target="">现任领导</a></div>
                                    <div class="btn btn-primary"><a href="../xxgl/lsyg.htm" target="">历史沿革</a></div>
                                    <div class="btn btn-primary"><a href="../xxgl/sfyx.htm" target="">三风一训</a></div>
                                    <div class="btn btn-primary"><a href="../xxgl/xydt.htm" target="">校园地图</a></div>
                                
                                    <div class="btn btn-primary"><a href="../xxgl/xyfg.htm" target="">校园风光</a></div>
                                </div>
                            </div>
                        </div>
                        <div class="sub_menu bind_menu_a" id="layer2" data-layerid="layer2" style="display: none;">
                            <i></i>
                            <div class="sub_area clearfix">
                                <div class="sub_img">
                                    <a title="" alt="" href="#"><img src="../images/menu2.jpg" class="img-responsive"></a>
                                </div>
                                <div class="sub_content">
                                        <h4>机构设置</h4>
                                        <p>辽宁铁道职业技术学院机构由党群行政机构、教学机构、教学辅助机构三类组成，共设置机构部门30个，其中党群行政机构16个、教学机构11个、教学辅助机构3个。</p>
                                        <div class="btn btn-info"><a href="../jgsz.htm" target="">详细介绍</a></div>
                                </div>
                                <div class="sub_btn">
                                    <div class="btn btn-primary"><a href="../jgsz/jxjg.htm" target="">教学机构</a></div>
                                    <div class="btn btn-primary"><a href="../jgsz/dzgljg.htm" target="">党政管理机构</a></div>
                                    <div class="btn btn-primary"><a href="../jgsz/ddjczzyqtzz.htm" target="">党的基层组织与群团组织</a></div>
                                    <div class="btn btn-primary"><a href="../jgsz/jyjxfzjg.htm" target="">教育教学辅助机构</a></div>
                                </div>
                            </div>
                        </div>
                        <div class="sub_menu bind_menu_a" id="layer3" data-layerid="layer3" style="display: none;">
                            <i></i>
                            <div class="sub_area clearfix">
                                <div class="sub_img">
                                    <a title="" alt="" href="#"><img src="../images/menu3.jpg" class="img-responsive"></a>
                                </div>
                                <div class="sub_content">
                                        <h4>教学科研</h4>
                                        <p>学校始终坚持“教学立校、科研兴校”的发展理念，形成了教学与科研相互促进、相互带动的良好氛围。升高职以来，累计完成市级及以上教科研课题238项；获得国家专利授权90项；软件著作权26项；公开出版教材226部；公开发表论文746篇，其中核心期刊35篇；获国家级教学成果二等奖1项，省级教学成果奖12项。</p>
                                        <div class="btn btn-info"><a href="../dhlm/jxky.htm">详细介绍</a></div>
                                </div>
                                <div class="sub_btn">
                                    <div class="btn btn-primary"><a href="http://www.lntdxy.com/jwc/">教务处</a></div>
                                    <div class="btn btn-primary"><a href="#">发展规划处</a></div>
                                    <div class="btn btn-primary"><a href="http://www.lntdxy.com/zlglc/">教学质量管理处</a></div>
                                    <div class="btn btn-primary"><a href="http://www.lntdxy.com/tsg/">图书馆</a></div>
                                    <div class="btn btn-primary"><a href="../jxzyk.jsp?urltype=tree.TreeTempUrl&amp;wbtreeid=1114" target="">教学资源库</a></div>
                                </div>
                            </div>
                        </div>
                        <div class="sub_menu bind_menu_a" id="layer4" data-layerid="layer4" style="display: none;">
                            <i></i>
                            <div class="sub_area clearfix">
                                <div class="sub_img">
                                    <a title="" alt="" href="#"><img src="../images/menu4.jpg" class="img-responsive"></a>
                                </div>
                                <div class="sub_content">
                                        <h4>招生就业</h4>
                                        <p>学校制定科学合理的招生计划和工作流程，单独招生报考年均4000人以上，普招录取分数线位居辽宁高职榜首。积极拓展就业市场，全方位开展就业指导服务，就业率一直保持在95%以上，对口就业率85%以上，已经形成就业率高、就业质量好、就业起薪高、就业稳定性强、就业工作发展前景好的良好就业格局。</p>
                                        <div class="btn btn-info"><a href="../dhlm/zsjy.htm">详细介绍</a></div>
                                </div>
                                <div class="sub_btn">
                                    <div class="btn btn-primary"><a href="http://www.lntdxy.com/zsxxw/">招生信息</a></div>
                                    <div class="btn btn-primary"><a href="#">就业信息</a></div>
                                    <div class="btn btn-primary"><a href="#">继续教育</a></div>
                                    <div class="btn btn-primary"><a href="#">培训服务</a></div>
                                </div>
                            </div>
                        </div>
                        <div class="sub_menu bind_menu_a" id="layer5" data-layerid="layer5" style="display: none;">
                            <i></i>
                            <div class="sub_area clearfix">
                                <div class="sub_img">
                                    <a title="" alt="" href="#"><img src="../images/menu5.jpg" class="img-responsive"></a>
                                </div>
                                <div class="sub_content">
                                        <h4>校企合作</h4>
                                        <p>校企合作本着"以服务为宗旨，以就业为导向"的方针，着眼于"精细化培养，高位化就业"的目标，加强优势互补，实现互惠共赢。做到学校与企业信息、资源共享，既能让学生在校所学与企业实践有机结合，又解决了企业人才培养的后顾之忧，节约了教育与企业成本，适应社会与市场需要。</p>
                                        <div class="btn btn-info"><a href="../dhlm/xqhz.htm">详细介绍</a></div>
                                </div>
                                <div class="sub_btn">
                                    <div class="btn btn-primary"><a href="#">一企三校职教集团</a></div>
                                    <div class="btn btn-primary"><a href="http://www.lntdxy.com/gdjt" target="">订单培养</a></div>
                                </div>
                            </div>
                        </div>
                        <div class="sub_menu bind_menu_a" id="layer6" data-layerid="layer6" style="display: none;">
                            <i></i>
                            <div class="sub_area clearfix">
                                <div class="sub_img">
                                    <a title="" alt="" href="#"><img src="../images/menu6.jpg" class="img-responsive"></a>
                                </div>
                                <div class="sub_content">
                                        <h4>学工在线</h4>
                                        <p>聚焦立德树人根本任务，主动适应铁路轨道交通行业需求，积极践行人民军队优良作风，凝炼构建了“1234”半军事化学生管理与服务体系，创新构建了“12306”共青团工作体系。学校团委获“全国五四红旗团委”“全国铁路五四红旗团委”荣誉称号。学校成功获批全国职业院校学生管理50强单位。</p>
                                        <div class="btn btn-info"><a href="../dhlm/xgzx.htm">详细介绍</a></div>
                                </div>
                                <div class="sub_btn">
                                    <div class="btn btn-primary"><a href="http://www.lntdxy.com/tuanw/">团委</a></div>
                                    <div class="btn btn-primary"><a href="http://www.lntdxy.com/xgzx/">学生处</a></div>
                                </div>
                            </div>
                        </div>
                    <div class="sub_menu bind_menu_a" id="layer7" data-layerid="layer7" style="display: none;">
                            <i></i>
                            <div class="sub_area clearfix">
                                <div class="sub_img">
                                    <a title="" alt="" href="#"><img src="../images/menu7.jpg" class="img-responsive"></a>
                                </div>
                                <div class="sub_content">
                                        <h4>信息公开</h4>
                                        <p>学校信息是指学校在开展办学活动和提供社会公共服务过程中产生、制作、获取的以一定形式记录、保存的信息。学校按照有关法律法规的规定予以公开。
学校信息的公开遵循以下原则：坚持党的领导，依法公开；信息的公开要公平、公正、便民。
学校根据《高等学校信息公开办法》要求，将属于主动公开的信息公开。</p>
                                        <div class="btn btn-info"><a href="../xxgk/xxgkzn.htm">详细介绍</a></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
         </div>  
       
        <div class="collapse navbar-collapse nav-menu" id="bs-example-navbar-collapse-1">
            <div class="container">
                <ul class="nav navbar-nav">
                    <li class="active">
                         <a href="../index.htm">网站首页</a>
                    </li>
                    <li class="dropdown">
                         <a href="#" class="dropdown-toggle" data-toggle="dropdown">学校概览<strong class="caret"></strong></a>
                        <ul class="dropdown-menu">
                            <li>
                                 <a href="../xxgl/xxjj.htm">学校简介</a>
                            </li>
                            <li>
                                 <a href="../xxgl/xxzc.htm">学校章程</a>
                            </li>
                            <li>
                                 <a href="../xxgl/xrld.htm">现任领导</a>
                            </li>
                            <li>
                                 <a href="../xxgl/lsyg.htm">历史沿革</a>
                            </li>
                            <li>
                                 <a href="../xxgl/sfyx.htm">三风一训</a>
                            </li>
                            <li>
                                 <a href="../xxgl/xydt.htm">校园地图</a>
                            </li>
                       
                            <li>
                                 <a href="../xxgl/xyfg.htm">校园风光</a>
                            </li>
                        </ul>
                    </li>
                    <li class="dropdown">
                         <a href="#" class="dropdown-toggle" data-toggle="dropdown">机构设置<strong class="caret"></strong></a>
                        <ul class="dropdown-menu">
                            <li>
                                 <a href="../jgsz/jxjg.htm">教学机构</a>
                            </li>
                             <li>
                                 <a href="../jgsz/dzgljg.htm">党政管理机构</a>
                            </li>
                            <li>
                                 <a href="../jgsz/ddjczzyqtzz.htm">党的基层组织与群团组织</a>
                            </li>
                            <li>
                                 <a href="../jgsz/jyjxfzjg.htm">教育教学辅助机构</a>
                            </li>
                        </ul>
                    </li>
                    <li class="dropdown">
                         <a href="#" class="dropdown-toggle" data-toggle="dropdown">教学科研<strong class="caret"></strong></a>
                        <ul class="dropdown-menu">
                            <li>
                                 <a href="http://www.lntdxy.com/jwc/">教务处</a>
                            </li>
                            <li>
                                 <a href="#">发展规划处</a>
                            </li>
                            <li>
                                 <a href="http://www.lntdxy.com/zlglc/">教学质量管理处</a>
                            </li>
                            <li>
                                 <a href="http://www.lntdxy.com/tsg/">图书馆</a>
                            </li>
                            <li>
                                 <a href="../jxzyk.jsp?urltype=tree.TreeTempUrl&amp;wbtreeid=1114">教学资源库</a>
                            </li>
                        </ul>
                    </li>
                    <li class="dropdown">
                         <a href="#" class="dropdown-toggle" data-toggle="dropdown">招生就业<strong class="caret"></strong></a>
                        <ul class="dropdown-menu">
                            <li>
                                 <a href="http://www.lntdxy.com/zsxxw/">招生信息</a>
                            </li>
                            <li>
                                 <a href="#">就业信息</a>
                            </li>
                            <li>
                                 <a href="#">继续教育</a>
                            </li>
                            <li>
                                 <a href="#">培训服务</a>
                            </li>
                        </ul>
                    </li>
                    <li class="dropdown">
                         <a href="#" class="dropdown-toggle" data-toggle="dropdown">校企合作<strong class="caret"></strong></a>
                        <ul class="dropdown-menu">
                            <li>
                                 <a href="#">一企三校职教集团</a>
                            </li>
                            <li>
                                 <a href="http://www.lntdxy.com/gdjt">订单培养</a>
                            </li>
                        </ul>
                    </li>
                    <li class="dropdown">
                         <a href="#" class="dropdown-toggle" data-toggle="dropdown">学工在线<strong class="caret"></strong></a>
                        <ul class="dropdown-menu">
                            <li>
                                 <a href="http://www.lntdxy.com/xgzx/">团委</a>
                            </li>
                            <li>
                                 <a href="http://www.lntdxy.com/xgzx/">学生处</a>
                            </li>
                        </ul>
                    </li>
                    <li>
                         <a href="../xxgk.htm">信息公开<strong class="caret"></strong></a>
                    </li>
                </ul>
            </div>
        </div></nav>
</div>

<div class="sec-bg1"></div>

<section class="subpage">
        <div class="container block">
            <div class="row clearfix">
                <div class="col-md-2">
                        <div class="panel">
                            <div class="panel-heading">
                                <p><i class="fa fa-book"></i></p>
                                <div>首页栏目</div>
                            </div>
                           <div>
    <div class="panel-body">
          <a href="tytt.htm">铁院头条</a>
     </div>

    <div class="panel-body">
          <a href="tydt.htm">铁院动态</a>
     </div>

    <div class="panel-body">
          <a href="tzgg.htm">通知公告</a>
     </div>

     <div class="panel-body">
          <a href="zbgg.htm" class="active">招标公告</a>
     </div>

    <div class="panel-body">
          <a href="zjrd.htm">职教热点</a>
     </div>

    <div class="panel-body">
          <a href="mtjj.htm">媒体聚焦</a>
     </div>
</div>
                          
                        </div>
                </div>
                <div class="col-md-10">
                    <div class="second-block">
                        <div class="title clearfix">
                            <ul class="breadcrumb">当前位置： 


                         网站首页&gt;
                            




                         首页栏目&gt;
                            




                         招标公告&gt;
                            

</ul>
                            <h3>招标公告</h3></div>
                        <div class="sec-list">

<script language="javascript" src="/system/resource/js/dynclicks.js"></script><script language="javascript" src="/system/resource/js/news/statpagedown.js"></script>
                                
<li id="line_u5_0">
                                    <a href="../info/1039/3201.htm">
                                        <img src="" class="img-responsive">
                                        <h4>询价公告</h4>
                                        
                                        <p class="date"><i class="fa fa-calendar"></i>2025-05-07</p>
                                        <p>询价公告我校有双凌校区北侧地块征占草地审批组卷项目，预算金额35000元。本着公平、公正原则，现向社会采用询价采购的方式确定项目服务企业，望有资质企业参与我校项目询价。项目具体内容及要求：辽宁铁道职业技...</p>
                                    </a>
                                </li>
                                
    <span id="section_u5_0" style="display:none;"><hr style="height:1px;border:none;border-top:1px dashed #CCCCCC;"></span>
<li id="line_u5_1">
                                    <a href="../info/1039/3194.htm">
                                        <img src="" class="img-responsive">
                                        <h4>询价公告（2025劳务派遣服务）</h4>
                                        
                                        <p class="date"><i class="fa fa-calendar"></i>2025-04-23</p>
                                        <p>询价公告&nbsp;我校有2025劳务派遣服务 项目，预算金额80元/人/月元，先需劳务派遣岗位24人左右。本着公平、公正原则，现向社会采用询价采购的方式确定项目服务企业，望有资质企业参与我校项目询价。现将有关事项说明...</p>
                                    </a>
                                </li>
                                
    <span id="section_u5_1" style="display:none;"><hr style="height:1px;border:none;border-top:1px dashed #CCCCCC;"></span>
<li id="line_u5_2">
                                    <a href="../info/1039/3193.htm">
                                        <img src="" class="img-responsive">
                                        <h4>辽宁铁道职业技术学院2025年大型客车（含司机）租赁服务采购...</h4>
                                        
                                        <p class="date"><i class="fa fa-calendar"></i>2025-04-23</p>
                                        <p>辽宁铁道职业技术学院2025年大型客车（含司机）租赁服务采购竞争性磋商公告项目概况：辽宁铁道职业技术学院2025年大型客车（含司机）租赁服务采购的潜在供应商应在辽宁隆森项目管理有限公司（锦州市凌河区解放东...</p>
                                    </a>
                                </li>
                                
    <span id="section_u5_2" style="display:none;"><hr style="height:1px;border:none;border-top:1px dashed #CCCCCC;"></span>
<li id="line_u5_3">
                                    <a href="../info/1039/3192.htm">
                                        <img src="" class="img-responsive">
                                        <h4>辽宁铁道职业技术学院2025年轿车、商务车租赁服务采购竞争性...</h4>
                                        
                                        <p class="date"><i class="fa fa-calendar"></i>2025-04-23</p>
                                        <p>&nbsp;辽宁铁道职业技术学院2025年轿车、商务车租赁服务采购竞争性谈判公告项目概况：辽宁铁道职业技术学院2025年轿车、商务车租赁服务采购的潜在供应商应在辽宁隆森项目管理有限公司（锦州市凌河区解放东路32-7号）获...</p>
                                    </a>
                                </li>
                                
    <span id="section_u5_3" style="display:none;"><hr style="height:1px;border:none;border-top:1px dashed #CCCCCC;"></span>
<li id="line_u5_4">
                                    <a href="../info/1039/3191.htm">
                                        <img src="" class="img-responsive">
                                        <h4>辽宁铁道职业技术学院校园超市委托管理服务采购项目的竞争性...</h4>
                                        
                                        <p class="date"><i class="fa fa-calendar"></i>2025-04-23</p>
                                        <p>辽宁铁道职业技术学院校园超市委托管理服务采购项目的竞争性谈判采购公告项目概况（辽宁铁道职业技术学院校园超市委托管理服务采购项目） 采购项目的潜在供应商应在锦州百众招投标代理有限公司获取采购文件，并于...</p>
                                    </a>
                                </li>
                                
    <span id="section_u5_4" style="display:none;"><hr style="height:1px;border:none;border-top:1px dashed #CCCCCC;"></span>

   <div class="pages"><link rel="stylesheet" content-type="text/css" href="/system/resource/css/pagedown/sys.css"><div class="pb_sys_common pb_sys_normal pb_sys_style1" style="margin-top:10px;text-align:center;"><span class="p_t">共52条</span> <span class="p_pages"><span class="p_first_d p_fun_d">首页</span><span class="p_prev_d p_fun_d">上页</span><span class="p_no_d">1</span><span class="p_no"><a href="zbgg/10.htm">2</a></span><span class="p_no"><a href="zbgg/9.htm">3</a></span><span class="p_no"><a href="zbgg/8.htm">4</a></span><span class="p_no"><a href="zbgg/7.htm">5</a></span><span class="p_dot">...</span><span class="p_no"><a href="zbgg/1.htm">11</a></span><span class="p_next p_fun"><a href="zbgg/10.htm">下页</a></span><span class="p_last p_fun"><a href="zbgg/1.htm">尾页</a></span></span> <span class="p_t">1/11</span></div>
              </div><script>_showDynClickBatch(['dynclicks_u5_3201','dynclicks_u5_3194','dynclicks_u5_3193','dynclicks_u5_3192','dynclicks_u5_3191'],[3201,3194,3193,3192,3191],"wbnews", 1632666717)</script></div>
                      
                    </div>
                </div>
            </div>
        </div>
    </section>


<div id="footer"><div class="container">
        <div class="row clearfix">
            <div class="col-md-6">
                <div class="row clearfix">
                    <div class="col-xs-12">
                     <img src="../images/logo-footer.png" class="img-responsive xs-hidden"> 
                      <div style="margin:0 auto;width:100%;text-align:center">
                     <span id="_ideConac"><a href="https://bszs.conac.cn/sitename?method=show&amp;id=A193492E7C1F052BE05310291AAC73CC" target="_blank">
                        <img id="imgConac" src="../images/blue.png" data-bd-imgshare-binded="1" vspace="0" hspace="0" border="0">
                   
                </a></span><span id="_ideConac"></span>
                </div></div>
                   <div class="col-xs-12">
                      <p class="first">版权所有：辽宁铁道职业技术学院</p>
                      <p>学院地址：辽宁省锦州市凌河区松坡里129号&nbsp;&nbsp;|&nbsp;&nbsp;邮编：121000</p>
                      <p>党政办电话：0416-3920425 0416-3920560</p>
                         <p><a href="https://beian.miit.gov.cn/">辽ICP备14002303号-2</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a target="_blank" href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=21070302000295" style="display:inline-block;text-decoration:none;height:20px;line-height:20px;"><img src="../images/1858301452.jpg" style="float:left;">&nbsp;辽公网安备 21070302000295号</a></p>
                    </div>
              </div>
            </div>
           <div class="col-md-3 footer-menu clearfix">
                  <a class="btn btn-primary" href="http://www.lntdxy.com/index.htm">网站首页</a>
                  <a class="btn btn-primary" href="http://www.lntdxy.com/xxgl/xxjj.htm">学校概览</a>
                  <a class="btn btn-primary" href="http://www.lntdxy.com/jgsz/dqxzjg.htm">机构设置</a>
                  <a class="btn btn-primary" href="http://www.lntdxy.com/dhlm/jxky.htm">教学科研</a>
                  <a class="btn btn-primary" href="http://www.lntdxy.com/dhlm/zsjy.htm">招生就业</a>
                  <a class="btn btn-primary" href="http://www.lntdxy.com/dhlm/xqhz.htm">校企合作</a>
                  <a class="btn btn-primary" href="http://www.lntdxy.com/dhlm/xgzx.htm">学工在线</a>
                  <a class="btn btn-primary" href="http://www.lntdxy.com/xxgk/xxgkzn.htm">信息公开</a>
            </div>
            <div class="col-md-3">
                <div class="row clearfix">
                    <div class="col-xs-6">
                        <div><img src="../images/ewm1.jpg" class="img-responsive"></div>
                        <p>官方微信</p>
                    </div>
                    <div class="col-xs-6">
                          <div><img src="../images/ewm2.jpg" class="img-responsive"></div>
                          <p>官方微博</p>
                    </div>
                </div>
            </div>
      </div>
   </div></div>

<div class="bottom-icon">
    <ul>
        <li><a href="#top"><i class="fa fa-arrow-up"></i></a></li>
        <li><a href="#footer" class="weixin"><i class="fa fa-weixin"></i>
        <div class="wxewm"><img src="../images/ewm3.jpg" class="img-responsive"></div></a>
        </li>
        <li><a href="https://weibo.com/u/6292259090" target="_blank"><i class="fa fa-weibo"></i></a></li>
    </ul>
</div>
    <script>
        $(function () {
            initNavMenuActive();

            $(".navbar-nav").on("mouseover", ".dropdown", function () {
                $(this).addClass("open");
            }).on("mouseleave", ".dropdown", function () {
                $(this).removeClass("open");
            });

            $(".nav-tabs").on("mouseover", "a[data-toggle=tab]", function () {
                $(this).tab("show");
            });

            $("#open-search").on("click", function () {
                $(".navbar-form").show();
            });
            $("#close-search").on("click", function () {
                $(".navbar-form").hide();
            });
        }); // end jQuery.reday

        function initNavMenuActive() {
            var url = location.pathname;
            if (url == "/") {
                $("#navbar-collapse-main > ul[class='nav navbar-nav'] > li:first")
                    .addClass("active");
            } else {
                var $a = $("#navbar-collapse-main > ul[class='nav navbar-nav'] a[href='" + url + "']"),
                    $li = $a.parentsUntil("#navbar-collapse-main > ul[class='nav navbar-nav']", "li.dropdown");
                if ($li.length == 0) {
                    $a.parent()
                        .addClass("active");
                } else {
                    $li.addClass("active");
                }
            }
        }
        function showHideLayer(layerid, actionid) {
            if (actionid == 'show') {
                $('#' + layerid).show();
            } else {
                $('#' + layerid).hide();
            }
        }
        
        function  init_nav() {
            $(".bind_menu_a").bind({
                mouseover: function(){
                    var $t = $(this);
                    var layerid = $t.data('layerid');
                    showHideLayer(layerid, 'show');
                },
                mouseout: function(){
                    var $t = $(this);
                    var layerid = $t.data('layerid');
                    showHideLayer(layerid, 'hide');
                }
            });
        }
        
        $(function(){
            init_nav();
        });

  </script>
  
  <!--百度推广代码-->

<script>
(function(){
    var bp = document.createElement('script');
    var curProtocol = window.location.protocol.split(':')[0];
    if (curProtocol === 'https') {
        bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
    }
    else {
        bp.src = 'http://push.zhanzhang.baidu.com/push.js';
    }
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(bp, s);
})();
</script>





<div id="wetab-content-root"><wetab-chat-screenshot style="position: relative; z-index: 2147483647;"></wetab-chat-screenshot><wetab-chat-contextmenu class="wetab-root" style="position: relative; z-index: 2147483647;"></wetab-chat-contextmenu></div></body>


'''


class WoCloudAI:
    def __init__(self):
        self.url = "https://panservice.mail.wo.cn/wohome/ai/assistant/query"
        self.x_yp_client_id = [
            "1001000035",
            "1001000036",
            "1001000037",
            "1001000021",
            "1001000022",
            "1001000023",
            "1001000024",
            "1001000025",
            "1001000026",
            "1001000027",
            "1001000028",
            "1001000029",
            "1001000030",
            "1001000031",
            "1001000032",
            "1001000033",
            "1001000034",
        ]
        self.user_agent = [
            "Mozilla/5.0 (Linux; Android 14; MEIZU 21 Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.64 Mobile Safari/537.36/woapp LianTongYunPan/3.0.14 (Android 14)",
            "Mozilla/5.0 (Linux; Android 13; Google Pixel 6 Build/TQ3A.230805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.170 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; Samsung Galaxy S21 Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/113.0.5672.92 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; OnePlus 9 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/112.0.5615.49 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; Xiaomi 13 Build/UP1A.230905.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.170 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; Huawei P40 Build/HUAWEIANA-LX4; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.77 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 9; Oppo Reno 3 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.124 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 8; Vivo X21 Build/O11019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.91 Mobile Safari/537.36",
        ]
        self.headers = {
            "Host": "panservice.mail.wo.cn",
            "Connection": "close",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Android WebView";v="127", "Chromium";v="127"',
            "X-YP-Access-Token": X_YP_Access_Token,
            "X-YP-App-Version": "3.0.14",
            "sec-ch-ua-mobile": "?1",
            "User-Agent": random.choice(self.user_agent),
            "Content-Type": "application/json",
            "accept": "text/event-stream",
            "X-YP-Client-Id": random.choice(self.x_yp_client_id),
            "sec-ch-ua-platform": '"Android"',
            "Origin": "https://panservice.mail.wo.cn",
            "X-Requested-With": "com.chinaunicom.bol.cloudapp",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://panservice.mail.wo.cn/h5/wocloud_ai/",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    def query(self, input_text="aaa",  model_id=0, tag=0, history=None):

        # model_id: 0 是默认模型，1 是 deepseek
        # input_text： 输入文本

        if history is None:
            history = []

        data = {"input": input_text, "modelId": model_id, "tag": tag, "history": history}

        try:
            response = requests.post(self.url, headers=self.headers, json=data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            full_response = ""  # Initialize an empty string to store the full response
            for line in response.iter_lines():
                decoded_line = line.decode("utf-8").replace("data:", "").strip()
                if len(decoded_line) != 0:
                    json_line = json.loads(decoded_line)  # Parse each line as JSON 
                    full_response += json_line["response"]  # Append the 'response' value
                    
            print("Full response:", full_response) 

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")


    def get_prompt(self, contents):

        prompt = """
        提取招标公告列表的XPath表达式，仅返回一个准确的XPath表达式，无需其他内容。

        目标元素特征：
        - 通常在列表结构中(如ul/li或table/tr)
        - 返回的必须是完整的列表项元素本身，而非其中的链接元素
        - 最多使用3个div层级，可以使用//跳过中间层级或使用特定的class属性直接定位

        分析此HTML并返回最简洁有效的XPath，确保表达式停止在列表项级别而不深入到子元素:
        {text}
        """
        return prompt.format(text=contents)
        

if __name__ == "__main__":

    ai = WoCloudAI()

    prompt = ai.get_prompt(contents)

    ai.query(input_text=prompt)  # Example usage




