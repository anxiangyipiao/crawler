import json
import requests
import random
import os





X_YP_Access_Token = "a36a90f6-d119-4b50-970f-30894a2f39fa"



contents = '''
<body>
  <div class="heade-top">
    <div class="top">
      <div class="container clearfix">
        <script language="javascript" src="/system/resource/js/dynclicks.js"></script><script language="javascript" src="/system/resource/js/openlink.js"></script>
<div class="pull-left top-one"><a href="#" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 66215)">国家双高计划建设院校</a></div>
<div class="pull-left top-tow"><a href="#" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 66216)">国家首批示范高职院校</a></div>




        <ul class="top-list pull-right clearfix">
    <li class="phone-li">
        <a href="https://ehall.whit.edu.cn" target="_blank" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 66219)" style="color:yellow;">办事大厅</a>
    </li>
    <li class="phone-li">
        <a href="https://mail.whit.edu.cn" target="_blank" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 66220)">电子邮箱</a>
    </li>
    <li class="phone-li">
        <a href="http://www.qggzszk.org" target="_blank" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 66221)">全国思政联盟网</a>
    </li>
    <li class="phone-li">
        <a href="https://lhtygtt.whit.edu.cn/" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 97020)">联合体与共同体</a>
    </li>
    <li class="phone-li">
        <a href="https://www.wvea.org.cn/" target="_blank" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 81928)">芜湖职业教育联盟</a>
    </li>
    <li class="phone-li">
        <a href="mailto:sjxz@whit.edu.cn" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 66222)">书记信箱</a>
    </li>
    <li class="phone-li">
        <a href="mailto:sjxz@whit.edu.cn" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 67560)">院长信箱</a>
    </li>
</ul>
      </div>
    </div>
    <div class="header">
      <div class="container">
        <div class="pull-left logo"><a href="../index.htm">        


                        <img src="../logo/logo-bai.svg" border="0" class="logo01">





                        <img src="../logo/logo-blue.svg" border="0" class="logo02">


</a></div>
        <div class="pull-right">
            <ul class="nav-list pull-left clearfix" id="pc">
                <li class="nav-list1">
    <a href="../xxgk.htm">学校概况</a><span class="nav-click"><span class="caret"></span></span>
    <div class="nav_child">
       <div class="item clearfix">
            <div class="l clearfix pull-left">
                <div class="pic pull-left"><img src="../dh/navpic2.png" alt=""></div>
                <div class="txt pull-right">
                <p>崇德     尚能</p>
                <p>务实     创新</p>
                <p></p>
                <p></p>
                </div>
            </div>
            <div class="r pull-right">     
              <a href="../xxgk/xxjj.htm">学校简介</a>   
              <a href="../xxgk/xrld.htm">现任领导</a>   
              <a href="../xxgk/jxry.htm">奖项荣誉</a>   
            </div>
        </div>
    </div>
</li>
<li class="nav-list1">
    <a href="../jgsz.htm">机构设置</a><span class="nav-click"><span class="caret"></span></span>
    <div class="nav_child">
       <div class="item clearfix">
            <div class="l clearfix pull-left">
                <div class="pic pull-left"><img src="../dh/jgszdh1.png" alt=""></div>
                <div class="txt pull-right">
                <p>遵循思政工作规律 </p>
                <p>遵循教书育人规律 </p>
                <p>遵循学生成长规律</p>
                <p></p>
                </div>
            </div>
            <div class="r pull-right">     
              <a href="../jgsz.htm#dq">党群机构</a>   
              <a href="../jgsz.htm#gl">管理机构</a>   
              <a href="../jgsz.htm#jx">教学机构</a>   
              <a href="../jgsz.htm#jf">教辅机构</a>   
              <a href="../jgsz.htm#fs">附属机构</a>   
            </div>
        </div>
    </div>
</li>
<li class="nav-list1">
    <a href="../rcpy.htm">人才培养</a><span class="nav-click"><span class="caret"></span></span>
    <div class="nav_child">
       <div class="item clearfix">
            <div class="l clearfix pull-left">
                <div class="pic pull-left"><img src="../dh/rcpysh.png" alt=""></div>
                <div class="txt pull-right">
                <p>落实立德树人根本任务 </p>
                <p>培养德智体美劳全面发展的社会主义建设者和接班人</p>
                <p></p>
                <p></p>
                </div>
            </div>
            <div class="r pull-right">     
              <a href="../rcpy/jyjx.htm">教育教学</a>   
              <a href="http://kczyw.whit.edu.cn/" target="_blank">课程资源</a>   
              <a href="../rcpy/szdw/qgyxjs.htm">师资队伍</a>   
              <a href="https://jxdd.whit.edu.cn/" target="_blank">质量监控</a>   
            </div>
        </div>
    </div>
</li>
<li class="nav-list1">
    <a href="../zsjy.htm">招生就业</a><span class="nav-click"><span class="caret"></span></span>
    <div class="nav_child">
       <div class="item clearfix">
            <div class="l clearfix pull-left">
                <div class="pic pull-left"><img src="../dh/zsjydh.png" alt=""></div>
                <div class="txt pull-right">
                <p>人人皆可成才</p>
                <p>人人尽展其才</p>
                <p></p>
                <p></p>
                </div>
            </div>
            <div class="r pull-right">     
              <a href="https://zs.whit.edu.cn" target="_blank">招生信息网</a>   
              <a href="https://jy.whit.edu.cn/" target="_blank">就业信息网</a>   
            </div>
        </div>
    </div>
</li>
<li class="nav-list1">
    <a href="../kxyj.htm">科学研究</a><span class="nav-click"><span class="caret"></span></span>
    <div class="nav_child">
       <div class="item clearfix">
            <div class="l clearfix pull-left">
                <div class="pic pull-left"><img src="../dh/kxyjdh.png" alt=""></div>
                <div class="txt pull-right">
                <p>产教研创</p>
                <p>深入融合</p>
                <p>协同推进</p>
                <p></p>
                </div>
            </div>
            <div class="r pull-right">     
              <a href="../kxyj/kydt.htm">科研动态</a>   
              <a href="../kxyj/kjfw.htm">科技服务</a>   
              <a href="../kxyj/kycg.htm">科研成果</a>   
              <a href="http://whzy.cbpt.cnki.net/EditorGN/index.aspx?t=1" target="_blank">芜职学报</a>   
              <a href="../kxyj/xmsb.htm">项目申报</a>   
            </div>
        </div>
    </div>
</li>
<li class="nav-list1">
    <a href="../jlhz.htm">交流合作</a><span class="nav-click"><span class="caret"></span></span>
    <div class="nav_child">
       <div class="item clearfix">
            <div class="l clearfix pull-left">
                <div class="pic pull-left"><img src="../navpic/navpic6.png" alt=""></div>
                <div class="txt pull-right">
                <p>创新人才培养模式</p>
                <p>提升校企合作质量</p>
                <p>不断提升服务经济发展能力</p>
                <p></p>
                </div>
            </div>
            <div class="r pull-right">     
              <a href="../jlhz/gjjlhz.htm">国际交流合作</a>   
              <a href="../jlhz/shjlhz.htm">社会交流合作</a>   
              <a href="https://xyh.whit.edu.cn/" target="_blank">校友会</a>   
            </div>
        </div>
    </div>
</li>
<li class="nav-list1">
    <a href="../jxjy1.htm">继续教育</a><span class="nav-click"><span class="caret"></span></span>
    <div class="nav_child">
       <div class="item clearfix">
            <div class="l clearfix pull-left">
                <div class="pic pull-left"><img src="../dh/jxjydh.png" alt=""></div>
                <div class="txt pull-right">
                <p>劳动光荣</p>
                <p>技能宝贵</p>
                <p>创造伟大</p>
                <p></p>
                </div>
            </div>
            <div class="r pull-right">     
              <a href="https://jxjy.whit.edu.cn/">继续教育网</a>   
              <a href="../jxjy1/shpx.htm">社会培训</a>   
              <a href="../jxjy1/xljy.htm">学历教育</a>   
              <a href="../jxjy1/jnrd.htm">技能认定</a>   
            </div>
        </div>
    </div>
</li>
<li class="nav-list1">
    <a href="../xsgz.htm">学生工作</a><span class="nav-click"><span class="caret"></span></span>
    <div class="nav_child">
       <div class="item clearfix">
            <div class="l clearfix pull-left">
                <div class="pic pull-left"><img src="../dh/xsgzdh.png" alt=""></div>
                <div class="txt pull-right">
                <p>锤炼品格</p>
                <p>学习知识</p>
                <p>创新思维</p>
                <p>奉献祖国</p>
                </div>
            </div>
            <div class="r pull-right">     
              <a href="../xsgz/xgdt.htm">学工动态</a>   
              <a href="https://xszz.whit.edu.cn/" target="_blank">学生资助</a>   
              <a href="https://xljk.whit.edu.cn/" target="_blank">心理健康</a>   
            </div>
        </div>
    </div>
</li>

            </ul>
            <ul class="nav-list pull-left clearfix" id="mobile">
                  

        <li>
            <a href="../xxgk.htm">学校概况</a><span class="nav-click"><span class="caret"></span></span>
                <ul class="nav-down" style="display:none;">
                        <li>
                            <a href="../xxgk/xxjj.htm">学校简介</a>
                        </li>
                        <li>
                            <a href="../xxgk/xrld.htm">现任领导</a>
                        </li>
                        <li>
                            <a href="../xxgk/jxry.htm">奖项荣誉</a>
                        </li>
                </ul>
        </li>

        <li>
            <a href="../jgsz.htm">机构设置</a><span class="nav-click"><span class="caret"></span></span>
                <ul class="nav-down" style="display:none;">
                        <li>
                            <a href="../jgsz.htm#dq">党群机构</a>
                        </li>
                        <li>
                            <a href="../jgsz.htm#gl">管理机构</a>
                        </li>
                        <li>
                            <a href="../jgsz.htm#jx">教学机构</a>
                        </li>
                        <li>
                            <a href="../jgsz.htm#jf">教辅机构</a>
                        </li>
                        <li>
                            <a href="../jgsz.htm#fs">附属机构</a>
                        </li>
                </ul>
        </li>

        <li>
            <a href="../rcpy.htm">人才培养</a><span class="nav-click"><span class="caret"></span></span>
                <ul class="nav-down" style="display:none;">
                        <li>
                            <a href="../rcpy/jyjx.htm">教育教学</a>
                        </li>
                        <li>
                            <a href="http://kczyw.whit.edu.cn/">课程资源</a>
                        </li>
                        <li>
                            <a href="../rcpy/szdw/qgyxjs.htm">师资队伍</a>
                        </li>
                        <li>
                            <a href="https://jxdd.whit.edu.cn/">质量监控</a>
                        </li>
                </ul>
        </li>

        <li>
            <a href="../zsjy.htm">招生就业</a><span class="nav-click"><span class="caret"></span></span>
                <ul class="nav-down" style="display:none;">
                        <li>
                            <a href="https://zs.whit.edu.cn">招生信息网</a>
                        </li>
                        <li>
                            <a href="https://jy.whit.edu.cn/">就业信息网</a>
                        </li>
                </ul>
        </li>

        <li>
            <a href="../kxyj.htm">科学研究</a><span class="nav-click"><span class="caret"></span></span>
                <ul class="nav-down" style="display:none;">
                        <li>
                            <a href="../kxyj/kydt.htm">科研动态</a>
                        </li>
                        <li>
                            <a href="../kxyj/kjfw.htm">科技服务</a>
                        </li>
                        <li>
                            <a href="../kxyj/kycg.htm">科研成果</a>
                        </li>
                        <li>
                            <a href="http://whzy.cbpt.cnki.net/EditorGN/index.aspx?t=1">芜职学报</a>
                        </li>
                        <li>
                            <a href="../kxyj/xmsb.htm">项目申报</a>
                        </li>
                </ul>
        </li>

        <li>
            <a href="../jlhz.htm">交流合作</a><span class="nav-click"><span class="caret"></span></span>
                <ul class="nav-down" style="display:none;">
                        <li>
                            <a href="../jlhz/gjjlhz.htm">国际交流合作</a>
                        </li>
                        <li>
                            <a href="../jlhz/shjlhz.htm">社会交流合作</a>
                        </li>
                        <li>
                            <a href="https://xyh.whit.edu.cn/">校友会</a>
                        </li>
                </ul>
        </li>

        <li>
            <a href="../jxjy1.htm">继续教育</a><span class="nav-click"><span class="caret"></span></span>
                <ul class="nav-down" style="display:none;">
                        <li>
                            <a href="https://jxjy.whit.edu.cn/">继续教育网</a>
                        </li>
                        <li>
                            <a href="../jxjy1/shpx.htm">社会培训</a>
                        </li>
                        <li>
                            <a href="../jxjy1/xljy.htm">学历教育</a>
                        </li>
                        <li>
                            <a href="../jxjy1/jnrd.htm">技能认定</a>
                        </li>
                </ul>
        </li>

        <li>
            <a href="../xsgz.htm">学生工作</a><span class="nav-click"><span class="caret"></span></span>
                <ul class="nav-down" style="display:none;">
                        <li>
                            <a href="../xsgz/xgdt.htm">学工动态</a>
                        </li>
                        <li>
                            <a href="https://xszz.whit.edu.cn/">学生资助</a>
                        </li>
                        <li>
                            <a href="https://xljk.whit.edu.cn/">心理健康</a>
                        </li>
                </ul>
        </li>







              <ul class="mobilelink">
    <li><a href="https://ehall.whit.edu.cn" target="_blank" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 66219)" style="color:yellow;">办事大厅</a></li>
    <li><a href="https://mail.whit.edu.cn" target="_blank" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 66220)" style="color:yellow;">电子邮箱</a></li>
    <li><a href="http://www.qggzszk.org" target="_blank" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 66221)" style="color:yellow;">全国思政联盟网</a></li>
    <li><a href="https://lhtygtt.whit.edu.cn/" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 97020)">联合体与共同体</a></li>
    <li><a href="https://www.wvea.org.cn/" target="_blank" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 81928)">芜湖职业教育联盟</a></li>
    <li><a href="mailto:sjxz@whit.edu.cn" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 66222)">书记信箱</a></li>
    <li><a href="mailto:sjxz@whit.edu.cn" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 67560)">院长信箱</a></li>
    <li><a href="https://news.whit.edu.cn/" target="_blank" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 66218)">新闻中心</a></li>
</ul>
            </ul>
          <div class="pull-left langer">
                <a href="https://english.whit.edu.cn/" target="_blank" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 66223)">En</a>

            <a class="search-a" role="button"><img class="logo01" src="../images/icon-ss.png"><img class="logo02" src="../images/icon-ss02.png"></a>
          </div>
        </div>
      </div>
      <div class="menu-button">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
      </div>
    </div>
  </div>
  <div class="search-box">
    <script type="text/javascript">
    function _nl_ys_check(){
        
        var keyword = document.getElementById('showkeycode271276').value;
        if(keyword==null||keyword==""){
            alert("请输入你要检索的内容！");
            return false;
        }
        if(window.toFF==1)
        {
            document.getElementById("lucenenewssearchkey271276").value = Simplized(keyword );
        }else
        {
            document.getElementById("lucenenewssearchkey271276").value = keyword;            
        }
        var  base64 = new Base64();
        document.getElementById("lucenenewssearchkey271276").value = base64.encode(document.getElementById("lucenenewssearchkey271276").value);
        new VsbFormFunc().disableAutoEnable(document.getElementById("showkeycode271276"));
        return true;
    } 
</script>
<div class="search-width">
<div style="    width: 700px;    margin: 0 auto;    background: #fff;    position: relative"><form action="../searchresult.jsp?wbtreeid=1026" method="post" id="au7a" name="au7a" onsubmit="return _nl_ys_check()">
 <input type="hidden" id="lucenenewssearchkey271276" name="lucenenewssearchkey" value=""><input type="hidden" id="_lucenesearchtype271276" name="_lucenesearchtype" value="1"><input type="hidden" id="searchScope271276" name="searchScope" value="1">
<input name="showkeycode" id="showkeycode271276" class="form-control">
<button class="btn btn-search  btnsearch" type="submit"></button> 
</form></div>
<div class="gb" style="position: absolute;right: 0;top: -90px;"><img src="../images/gb.png"></div>
</div><script language="javascript" src="/system/resource/js/base64.js"></script><script language="javascript" src="/system/resource/js/formfunc.js"></script>

  </div>
  <div class="js-banner wow fadeInUp animated" style="visibility: visible;"><img src="../images/js-banner.png"></div>
  <div class="container page-box container-sm clearfix">
    <div class="pull-left list-left wow fadeInUp animated" style="visibility: visible;">
        



<div class="list-left-top">招采与资产</div>
      
<ul class="list-left-nav">
    <li class="active">
        <a href="zcyzc.htm">招采与资产</a>
    </li>
    <li>
        <a href="yjsgk.htm">预决算公开</a>
    </li>
</ul>

    </div>
    <div class="pull-right right-box">
      <div class="nav-address wow fadeInUp animated" style="visibility: visible;"><a class="hidden-xs">您现在的位置： </a>
    <a href="../index.htm">首页</a>
    -&gt;
    <a href="zcyzc.htm" style="color:#055286;">招采与资产</a>
</div>
      <div class="page-title wow fadeInUp animated" style="visibility: visible;"><span><font>



招采与资产
</font></span></div>
      

<script language="javascript" src="/system/resource/js/centerCutImg.js"></script><script language="javascript" src="/system/resource/js/ajax.js"></script><ul class="list-ul wow fadeInUp animated" style="visibility: visible;">
    <li class="txt-elise">
    
        <a href="../info/1026/25525.htm" target="_blank">【中标公示】芜湖职业技术学院2025-2027年毕业生培养质量评价方案编制项目中标结果公告</a><span>2025-04-25</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/25347.htm" target="_blank">【中标公示】芜湖职业技术学院2024年电气与自动化学院高速芯片测试机应用系统采购项目中标结果公告</a><span>2025-04-08</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/25322.htm" target="_blank">【中标候选人公示】芜湖职业技术学院2024年电气与自动化学院高速芯片测试机应用系统采购项目中标候选人...</a><span>2025-04-03</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/25379.htm" target="_blank">【招标公示】芜湖职业技术学院2025-2027年毕业生培养质量评价方案编制项目公开招标公告</a><span>2025-04-03</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/25266.htm" target="_blank">【中标公示】芜湖职业技术学院2025年校园树木花卉种植项目中标结果公告</a><span>2025-03-31</span>
        
    </li>
</ul>
<ul class="list-ul wow fadeInUp animated" style="visibility: visible;">
    <li class="txt-elise">
    
        <a href="../info/1026/25268.htm" target="_blank">【中标公示】芜湖职业技术学院2025学校新建基本建设项目跟踪审计服务项目成交结果公告</a><span>2025-03-31</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/25204.htm" target="_blank">【中标公示】芜湖职业技术学院2025年-2028年教育网接入服务项目成交结果公告</a><span>2025-03-25</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/25147.htm" target="_blank">【单一来源邀请函】芜湖职业技术学院2025年-2028年教育网接入服务项目单一来源采购邀请函</a><span>2025-03-18</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/25139.htm" target="_blank">【招标公示】芜湖职业技术学院2025学校新建基本建设项目跟踪审计服务项目竞争性磋商公告</a><span>2025-03-17</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/25003.htm" target="_blank">【澄清公告】芜湖职业技术学院2025年校园树木花卉种植项目澄清公告</a><span>2025-03-14</span>
        
    </li>
</ul>
<ul class="list-ul wow fadeInUp animated" style="visibility: visible;">
    <li class="txt-elise">
    
        <a href="../info/1026/25000.htm" target="_blank">【中标公示】芜湖职业技术学院信息与人工智能学院2024年虚拟现实工程技术实训套装采购项目中标结果公告</a><span>2025-03-13</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/24839.htm" target="_blank">【招标公示】芜湖职业技术学院2024年电气与自动化学院高速芯片测试机应用系统采购项目公开招标公告</a><span>2025-03-12</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/24681.htm" target="_blank">【招标公示】芜湖职业技术学院2025年校园树木花卉种植项目公开招标公告</a><span>2025-03-07</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/24673.htm" target="_blank">【单一来源公示】芜湖职业技术学院2025年-2028年教育网接入服务项目单一来源公示</a><span>2025-03-06</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/24636.htm" target="_blank">【中标公示】芜湖职业技术学院2024年度食品与生物工程学院大型分析仪器仿真软件采购项目（二次）中标结...</a><span>2025-03-03</span>
        
    </li>
</ul>
<ul class="list-ul wow fadeInUp" style="visibility: hidden; animation-name: none;">
    <li class="txt-elise">
    
        <a href="../info/1026/24501.htm" target="_blank">【招标公示】芜湖职业技术学院信息与人工智能学院2024年虚拟现实工程技术实训套装采购项目公开招标公告</a><span>2025-02-19</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/24486.htm" target="_blank">【项目终止公告】芜湖职业技术学院2025分类考试招生进高中（中职）宣传活动服务项目终止公告</a><span>2025-02-17</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/24470.htm" target="_blank">【流标公示】芜湖职业技术学院2025分类考试招生进高中（中职）宣传活动服务项目流标公告</a><span>2025-02-14</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/24471.htm" target="_blank">【中标公示】芜湖职业技术学院2024年度校园消防设施零星维修耗材采购项目中标结果公告</a><span>2025-02-14</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/24442.htm" target="_blank">【招标公示】芜湖职业技术学院2024年度食品与生物工程学院大型分析仪器仿真软件采购项目（二次）招标公...</a><span>2025-02-07</span>
        
    </li>
</ul>
<ul class="list-ul wow fadeInUp" style="visibility: hidden; animation-name: none;">
    <li class="txt-elise">
    
        <a href="../info/1026/24424.htm" target="_blank">【招标公示】芜湖职业技术学院2025分类考试招生进高中（中职）宣传活动服务项目公开招标公告</a><span>2025-01-23</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/24425.htm" target="_blank">【流标公示】芜湖职业技术学院2024年度食品与生物工程学院大型分析仪器仿真软件采购项目终止公告</a><span>2025-01-23</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/24409.htm" target="_blank">【中标公示】芜湖职业技术学院2024年全国数字校园试点校融合数据基座建设及数据治理项目监理服务中标结...</a><span>2025-01-17</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/24408.htm" target="_blank">【中标公示】芜湖职业技术学院信息与人工智能学院2024年物联网实训应用平台采购项目中标结果公告</a><span>2025-01-17</span>
        
    </li>
    <li class="txt-elise">
    
        <a href="../info/1026/24398.htm" target="_blank">【招标公示】芜湖职业技术学院2024年度校园消防设施零星维修耗材采购项目公开招标公告</a><span>2025-01-15</span>
        
    </li>
</ul>
<div class="text-center">
    <div class="page-box-fy wow fadeInUp clearfix" style="visibility: hidden; animation-name: none;">
        <div class="page_pc">
            <link rel="stylesheet" content-type="text/css" href="/system/resource/css/pagedown/sys.css"><div class="pb_sys_common pb_sys_full pb_sys_style1" style="margin-top:10px;text-align:center;"><span class="p_pages"><span class="p_first_d p_fun_d">首页</span><span class="p_prev_d p_fun_d">上页</span><span class="p_no_d">1</span><span class="p_no"><a href="zcyzc/30.htm">2</a></span><span class="p_no"><a href="zcyzc/29.htm">3</a></span><span class="p_no"><a href="zcyzc/28.htm">4</a></span><span class="p_no"><a href="zcyzc/27.htm">5</a></span><span class="p_dot">...</span><span class="p_no"><a href="zcyzc/1.htm">31</a></span><span class="p_next p_fun"><a href="zcyzc/30.htm">下页</a></span><span class="p_last p_fun"><a href="zcyzc/1.htm">尾页</a></span></span> <span class="p_t">共31页</span> <span class="p_t">到第</span><span class="p_goto"><script language="javascript" src="/system/resource/js/gotopage.js"></script><input type="text" class="p_goto_input" maxlength="10" id="u13_goto" onkeydown="if(event.keyCode==13){_simple_list_gotopage_fun(31,&quot;u13_goto&quot;,2)}" spellcheck="false"></span><span class="p_t">页</span> <span class="p_goto"><a href="javascript:;" onclick="_simple_list_gotopage_fun(31,&quot;u13_goto&quot;,2)">跳转</a></span></div>
        </div>
        <div class="page_mob">
            <link rel="stylesheet" content-type="text/css" href="/system/resource/css/pagedown/sys.css"><div class="pb_sys_common pb_sys_short pb_sys_style1" style="margin-top:10px;text-align:center;"><span class="p_pages"><span class="p_first_d p_fun_d">首页</span><span class="p_prev_d p_fun_d">上页</span><span class="p_no_d">1</span><span class="p_no"><a href="zcyzc/30.htm">2</a></span><span class="p_no"><a href="zcyzc/29.htm">3</a></span><span class="p_no"><a href="zcyzc/28.htm">4</a></span><span class="p_no"><a href="zcyzc/27.htm">5</a></span><span class="p_dot">...</span><span class="p_no"><a href="zcyzc/1.htm">31</a></span><span class="p_next p_fun"><a href="zcyzc/30.htm">下页</a></span><span class="p_last p_fun"><a href="zcyzc/1.htm">尾页</a></span></span></div>
        </div>
    </div>
</div><script>_showDynClickBatch(['dynclicks_u13_25525','dynclicks_u13_25347','dynclicks_u13_25322','dynclicks_u13_25379','dynclicks_u13_25266','dynclicks_u13_25268','dynclicks_u13_25204','dynclicks_u13_25147','dynclicks_u13_25139','dynclicks_u13_25003','dynclicks_u13_25000','dynclicks_u13_24839','dynclicks_u13_24681','dynclicks_u13_24673','dynclicks_u13_24636','dynclicks_u13_24501','dynclicks_u13_24486','dynclicks_u13_24470','dynclicks_u13_24471','dynclicks_u13_24442','dynclicks_u13_24424','dynclicks_u13_24425','dynclicks_u13_24409','dynclicks_u13_24408','dynclicks_u13_24398'],[25525,25347,25322,25379,25266,25268,25204,25147,25139,25003,25000,24839,24681,24673,24636,24501,24486,24470,24471,24442,24424,24425,24409,24408,24398],"wbnews", 1655460640)</script>
      
    
      
      
      
    </div>
  </div>
  <div class="footer wow fadeInUp" style="visibility: hidden; animation-name: none;">
    <div class="container clearfix">
      <div class="pull-left logo-sm">    
    

                        <a href="../index.htm" title="" onclick="_addDynClicks(&quot;wbimage&quot;, 1655460640, 57485)" target="_blank">
                            <img src="../images/logo-sm.png" border="0">
                        </a>  


</div>
      <div class="pull-left footer-xq">
        <p>银湖校区<span>安徽省芜湖市银湖北路62号 </span><font>邮编：241006</font></p>
<p>文津校区<span>安徽省芜湖市文津西路201号</span><font>邮编：241003</font></p>
<p>白马校区<span>安徽省芜湖市长江南路与白马山路交汇处</span><font>邮编：241002</font></p>
<p>南陵校区<span>安徽省芜湖市南陵县龙池路1号</span><font>邮编：241300</font></p>
      </div>
      <ul class="pull-left footer-down">
        <li>
          <a href="../yqlj1.htm" onclick="_addDynClicks(&quot;wburl&quot;, 1655460640, 66534)">友情链接</a>

        </li>
      </ul>
      <div class="pull-right ewm-box text-center">
                    <div class="pull-left">
                    <img src="../images/sina_code.png" border="0" width="72" height="72"><br>官方微博
        </div>
        <div class="pull-left">
                    <img src="../images/guanfangweixin.jpg" border="0" width="72" height="72"><br>官方微信
        </div>
        <div class="pull-left">
                    <img src="../images/zhihuixiaoyuan.jpg" border="0" width="72" height="72"><br>智慧校园
        </div>

      </div>
    </div>
    <div class="container">
      <div class="footer-bottom">
        <span><img src="../images/footer01.png">版权所有©芜湖职业技术学院</span>
<span><img src="../images/footer02.png"><a href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=34020302000114" target="_blank">皖公网安备 34020302000114号</a></span>
        <!-- 版权内容请在本组件"内容配置-版权"处填写 -->
<p>
    <span><a href="https://beian.miit.gov.cn/#/Integrated/index" target="_blank">皖ICP备05000975号-3</a></span>
</p>
        
       
        
        
      </div>
    </div>
  <!--<a class="go-top"></a>-->
  </div>
      <!--<ul class="fix-ul">
<li>
<a href="https://my.whit.edu.cn" title="办事大厅" onclick="_addDynClicks(&#34;wbimage&#34;, 1655460640, 57490)" target="_blank" class="fix01">
<img src="../images/fix02.png" border="0"><br>办事大厅
</a>  
</li>
<li>
<a href="../xysh/wzxl.htm" title="芜职校历" onclick="_addDynClicks(&#34;wbimage&#34;, 1655460640, 57491)" target="_blank" class="fix02">
<img src="../images/fix03.png" border="0"><br>芜职校历
</a>  
</li>
</ul>
-->









<script src="../js/jquery.min.js"></script><script src="../js/bootstrap.min.js"></script><script src="../js/slick.js"></script><script src="../js/wow.min.js"></script><script src="../js/brief.js"></script><script>
if (!(/msie [6|7|8|9]/i.test(navigator.userAgent))){
  new WOW().init();
};
 $(".go-top").click(function() {
      $("html,body").animate({scrollTop:0}, 500);
  }); 
  //下滑导航加背景
window.onscroll=function(){ 
    var t=document.documentElement.scrollTop||document.body.scrollTop;  
    var div2=document.getElementById("header"); 
    if(t>= 50){ 
        $(".header").addClass("active");
    }else{
        $(".header").removeClass("active");
    } 
}
//搜索弹窗
  $(".search-a").click(function(){
          if($(".search-box").is(":hidden"))
          {
            $(".search-box").slideDown("slow");  
          }else{
            $(".search-box").slideUp("slow");
              }
  }); 
  
  $(".gb").click(function(){
  $(".search-box").hide();
}) 
var clicktag = 0;
$(".menu-button").click(function(){
if (clicktag == 0) {
  clicktag = 1;
  $(".nav-down").slideUp("slow");
  $(".nav-click").removeClass("active");
  $(this).toggleClass("cross");
  if($("#mobile").is(":hidden"))
  {
    $("#mobile").slideDown("slow");  
  }else{
    $("#mobile").slideUp("slow");
      }
  setTimeout(function () { clicktag = 0 }, 700);
}

}); 
  $(".nav-click").click(function(){
          if($(this).parents("li").find(".nav-down").is(":hidden"))
          {
            $(".nav-click").removeClass("active");
            $(this).addClass("active");
            $(".nav-down").slideUp("slow");
            $(this).parents("li").find(".nav-down").slideDown("slow");  
          }else{
            $(this).parents("li").find(".nav-down").slideUp("slow");
            $(this).removeClass("active");
              }
  });
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
        - 使用最简洁的表达式，尽量减少div层级，可以使用//跳过中间层级或使用特定的class属性直接定位

        分析此HTML并返回最简洁有效的XPath，确保表达式停止在列表项级别而不深入到子元素:
        {text}
        """
        return prompt.format(text=contents)
        

if __name__ == "__main__":

    ai = WoCloudAI()

    prompt = ai.get_prompt(contents)

    ai.query(input_text=prompt)  # Example usage




