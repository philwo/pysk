function rcube_webmail(){
this.env=new Object();
this.labels=new Object();
this.buttons=new Object();
this.buttons_sel=new Object();
this.gui_objects=new Object();
this.gui_containers=new Object();
this.commands=new Object();
this.command_handlers=new Object();
this.onloads=new Array();
this.ref="rcmail";
var _1=this;
this.dblclick_time=500;
this.message_time=3000;
this.identifier_expr=new RegExp("[^0-9a-z-_]","gi");
this.mimetypes=new Array("text/plain","text/html","text/xml","image/jpeg","image/gif","image/png","application/x-javascript","application/pdf","application/x-shockwave-flash");
this.env.keep_alive=60;
this.env.request_timeout=180;
this.env.draft_autosave=0;
this.env.comm_path="./";
this.env.bin_path="./bin/";
this.env.blankpage="program/blank.gif";
jQuery.ajaxSetup({cache:false,error:function(_2,_3,_4){
_1.http_error(_2,_3,_4);
},beforeSend:function(_5){
_5.setRequestHeader("X-RoundCube-Request",_1.env.request_token);
}});
this.set_env=function(p,_7){
if(p!=null&&typeof (p)=="object"&&!_7){
for(var n in p){
this.env[n]=p[n];
}
}else{
this.env[p]=_7;
}
};
this.add_label=function(_9,_a){
this.labels[_9]=_a;
};
this.register_button=function(_b,id,_d,_e,_f,_10){
if(!this.buttons[_b]){
this.buttons[_b]=new Array();
}
var _11={id:id,type:_d};
if(_e){
_11.act=_e;
}
if(_f){
_11.sel=_f;
}
if(_10){
_11.over=_10;
}
this.buttons[_b][this.buttons[_b].length]=_11;
};
this.gui_object=function(_12,id){
this.gui_objects[_12]=id;
};
this.gui_container=function(_14,id){
this.gui_containers[_14]=id;
};
this.add_element=function(elm,_17){
if(this.gui_containers[_17]&&this.gui_containers[_17].jquery){
this.gui_containers[_17].append(elm);
}
};
this.register_command=function(_18,_19,_1a){
this.command_handlers[_18]=_19;
if(_1a){
this.enable_command(_18,true);
}
};
this.add_onload=function(f){
this.onloads[this.onloads.length]=f;
};
this.init=function(){
var p=this;
this.task=this.env.task;
if(!bw.dom||!bw.xmlhttp_test()){
this.goto_url("error","_code=0x199");
return;
}
for(var n in this.gui_containers){
this.gui_containers[n]=$("#"+this.gui_containers[n]);
}
for(var n in this.gui_objects){
this.gui_objects[n]=rcube_find_object(this.gui_objects[n]);
}
this.init_buttons();
if(this.env.framed&&parent.rcmail&&parent.rcmail.set_busy){
parent.rcmail.set_busy(false);
}
this.enable_command("logout","mail","addressbook","settings",true);
if(this.env.permaurl){
this.enable_command("permaurl",true);
}
switch(this.task){
case "mail":
if(this.gui_objects.messagelist){
this.message_list=new rcube_list_widget(this.gui_objects.messagelist,{multiselect:true,draggable:true,keyboard:true,dblclick_time:this.dblclick_time});
this.message_list.row_init=function(o){
p.init_message_row(o);
};
this.message_list.addEventListener("dblclick",function(o){
p.msglist_dbl_click(o);
});
this.message_list.addEventListener("keypress",function(o){
p.msglist_keypress(o);
});
this.message_list.addEventListener("select",function(o){
p.msglist_select(o);
});
this.message_list.addEventListener("dragstart",function(o){
p.drag_start(o);
});
this.message_list.addEventListener("dragmove",function(e){
p.drag_move(e);
});
this.message_list.addEventListener("dragend",function(e){
p.drag_end(e);
});
document.onmouseup=function(e){
return p.doc_mouse_up(e);
};
this.message_list.init();
this.enable_command("toggle_status","toggle_flag",true);
if(this.gui_objects.mailcontframe){
this.gui_objects.mailcontframe.onmousedown=function(e){
return p.click_on_list(e);
};
}else{
this.message_list.focus();
}
}
if(this.env.coltypes){
this.set_message_coltypes(this.env.coltypes);
}
this.enable_command("list","checkmail","compose","add-contact","search","reset-search","collapse-folder",true);
if(this.env.search_text!=null&&document.getElementById("quicksearchbox")!=null){
document.getElementById("quicksearchbox").value=this.env.search_text;
}
if(this.env.action=="show"||this.env.action=="preview"){
this.enable_command("show","reply","reply-all","forward","moveto","delete","open","mark","edit","viewsource","download","print","load-attachment","load-headers",true);
if(this.env.next_uid){
this.enable_command("nextmessage",true);
this.enable_command("lastmessage",true);
}
if(this.env.prev_uid){
this.enable_command("previousmessage",true);
this.enable_command("firstmessage",true);
}
if(this.env.blockedobjects){
if(this.gui_objects.remoteobjectsmsg){
this.gui_objects.remoteobjectsmsg.style.display="block";
}
this.enable_command("load-images","always-load",true);
}
}
if(this.env.trash_mailbox&&this.env.mailbox!=this.env.trash_mailbox){
this.set_alttext("delete","movemessagetotrash");
}
if(this.env.action=="preview"&&this.env.framed&&parent.rcmail){
this.enable_command("compose","add-contact",false);
parent.rcmail.show_contentframe(true);
}
if(this.env.action=="compose"){
this.enable_command("add-attachment","send-attachment","remove-attachment","send",true);
if(this.env.spellcheck){
this.env.spellcheck.spelling_state_observer=function(s){
_1.set_spellcheck_state(s);
};
this.set_spellcheck_state("ready");
if($("input[name='_is_html']").val()=="1"){
this.display_spellcheck_controls(false);
}
}
if(this.env.drafts_mailbox){
this.enable_command("savedraft",true);
}
document.onmouseup=function(e){
return p.doc_mouse_up(e);
};
this.init_messageform();
}
if(this.env.messagecount){
this.enable_command("select-all","select-none","expunge",true);
}
if(this.purge_mailbox_test()){
this.enable_command("purge",true);
}
this.set_page_buttons();
if(this.env.action=="print"){
window.print();
}
if(this.gui_objects.mailboxlist){
this.env.unread_counts={};
this.gui_objects.folderlist=this.gui_objects.mailboxlist;
this.http_request("getunread","");
}
if(this.env.mdn_request&&this.env.uid){
var _29="_uid="+this.env.uid+"&_mbox="+urlencode(this.env.mailbox);
if(confirm(this.get_label("mdnrequest"))){
this.http_post("sendmdn",_29);
}else{
this.http_post("mark",_29+"&_flag=mdnsent");
}
}
break;
case "addressbook":
if(this.gui_objects.contactslist){
this.contact_list=new rcube_list_widget(this.gui_objects.contactslist,{multiselect:true,draggable:true,keyboard:true});
this.contact_list.row_init=function(row){
p.triggerEvent("insertrow",{cid:row.uid,row:row});
};
this.contact_list.addEventListener("keypress",function(o){
p.contactlist_keypress(o);
});
this.contact_list.addEventListener("select",function(o){
p.contactlist_select(o);
});
this.contact_list.addEventListener("dragstart",function(o){
p.drag_start(o);
});
this.contact_list.addEventListener("dragmove",function(e){
p.drag_move(e);
});
this.contact_list.addEventListener("dragend",function(e){
p.drag_end(e);
});
this.contact_list.init();
if(this.env.cid){
this.contact_list.highlight_row(this.env.cid);
}
if(this.gui_objects.contactslist.parentNode){
this.gui_objects.contactslist.parentNode.onmousedown=function(e){
return p.click_on_list(e);
};
document.onmouseup=function(e){
return p.doc_mouse_up(e);
};
}else{
this.contact_list.focus();
}
this.gui_objects.folderlist=this.gui_objects.contactslist;
}
this.set_page_buttons();
if(this.env.address_sources&&this.env.address_sources[this.env.source]&&!this.env.address_sources[this.env.source].readonly){
this.enable_command("add",true);
}
if(this.env.cid){
this.enable_command("show","edit",true);
}
if((this.env.action=="add"||this.env.action=="edit")&&this.gui_objects.editform){
this.enable_command("save",true);
}else{
this.enable_command("search","reset-search","moveto","import",true);
}
if(this.contact_list&&this.contact_list.rowcount>0){
this.enable_command("export",true);
}
this.enable_command("list",true);
break;
case "settings":
this.enable_command("preferences","identities","save","folders",true);
if(this.env.action=="identities"){
this.enable_command("add",this.env.identities_level<2);
}else{
if(this.env.action=="edit-identity"||this.env.action=="add-identity"){
this.enable_command("add",this.env.identities_level<2);
this.enable_command("save","delete","edit",true);
}else{
if(this.env.action=="folders"){
this.enable_command("subscribe","unsubscribe","create-folder","rename-folder","delete-folder",true);
}
}
}
if(this.gui_objects.identitieslist){
this.identity_list=new rcube_list_widget(this.gui_objects.identitieslist,{multiselect:false,draggable:false,keyboard:false});
this.identity_list.addEventListener("select",function(o){
p.identity_select(o);
});
this.identity_list.init();
this.identity_list.focus();
if(this.env.iid){
this.identity_list.highlight_row(this.env.iid);
}
}else{
if(this.gui_objects.sectionslist){
this.sections_list=new rcube_list_widget(this.gui_objects.sectionslist,{multiselect:false,draggable:false,keyboard:false});
this.sections_list.addEventListener("select",function(o){
p.section_select(o);
});
this.sections_list.init();
this.sections_list.focus();
this.sections_list.select("general");
}else{
if(this.gui_objects.subscriptionlist){
this.init_subscription_list();
}
}
}
break;
case "login":
var _34=$("#rcmloginuser");
_34.bind("keyup",function(e){
return rcmail.login_user_keyup(e);
});
if(_34.val()==""){
_34.focus();
}else{
$("#rcmloginpwd").focus();
}
$("#rcmlogintz").val(new Date().getTimezoneOffset()/-60);
this.enable_command("login",true);
break;
default:
break;
}
this.loaded=true;
if(this.pending_message){
this.display_message(this.pending_message[0],this.pending_message[1]);
}
if(this.gui_objects.folderlist){
this.gui_containers.foldertray=$(this.gui_objects.folderlist);
}
this.triggerEvent("init",{task:this.task,action:this.env.action});
for(var i=0;i<this.onloads.length;i++){
if(typeof (this.onloads[i])=="string"){
eval(this.onloads[i]);
}else{
if(typeof (this.onloads[i])=="function"){
this.onloads[i]();
}
}
}
this.start_keepalive();
};
this.start_keepalive=function(){
if(this.env.keep_alive&&!this.env.framed&&this.task=="mail"&&this.gui_objects.mailboxlist){
this._int=setInterval(function(){
_1.check_for_recent(false);
},this.env.keep_alive*1000);
}else{
if(this.env.keep_alive&&!this.env.framed&&this.task!="login"){
this._int=setInterval(function(){
_1.send_keep_alive();
},this.env.keep_alive*1000);
}
}
};
this.init_message_row=function(row){
var uid=row.uid;
if(uid&&this.env.messages[uid]){
row.deleted=this.env.messages[uid].deleted?true:false;
row.unread=this.env.messages[uid].unread?true:false;
row.replied=this.env.messages[uid].replied?true:false;
row.flagged=this.env.messages[uid].flagged?true:false;
row.forwarded=this.env.messages[uid].forwarded?true:false;
}
if(row.icon=row.obj.getElementsByTagName("td")[0].getElementsByTagName("img")[0]){
var p=this;
row.icon.id="msgicn_"+row.uid;
row.icon._row=row.obj;
row.icon.onmousedown=function(e){
p.command("toggle_status",this);
};
}
if(!this.env.flagged_col&&this.env.coltypes){
var _3b;
if((_3b=find_in_array("flag",this.env.coltypes))>=0){
this.set_env("flagged_col",_3b+1);
}
}
if(this.env.flagged_col&&(row.flagged_icon=row.obj.getElementsByTagName("td")[this.env.flagged_col].getElementsByTagName("img")[0])){
var p=this;
row.flagged_icon.id="flaggedicn_"+row.uid;
row.flagged_icon._row=row.obj;
row.flagged_icon.onmousedown=function(e){
p.command("toggle_flag",this);
};
}
this.triggerEvent("insertrow",{uid:uid,row:row});
};
this.init_messageform=function(){
if(!this.gui_objects.messageform){
return false;
}
var _3d=$("[name='_from']");
var _3e=$("[name='_to']");
var _3f=$("input[name='_subject']");
var _40=$("[name='_message']").get(0);
this.init_address_input_events(_3e);
this.init_address_input_events($("[name='_cc']"));
this.init_address_input_events($("[name='_bcc']"));
if(_3d.attr("type")=="select-one"&&$("input[name='_draft_saveid']").val()==""&&$("input[name='_is_html']").val()!="1"){
this.change_identity(_3d[0]);
}
if(_3e.val()==""){
_3e.focus();
}else{
if(_3f.val()==""){
_3f.focus();
}else{
if(_40){
_40.focus();
}
}
}
this.compose_field_hash(true);
this.auto_save_start();
};
this.init_address_input_events=function(obj){
var _42=function(e){
return _1.ksearch_keypress(e,this);
};
obj.bind((bw.safari||bw.ie?"keydown":"keypress"),_42);
obj.attr("autocomplete","off");
};
this.command=function(_44,_45,obj){
if(obj&&obj.blur){
obj.blur();
}
if(this.busy){
return false;
}
if(!this.commands[_44]){
if(this.env.framed&&parent.rcmail&&parent.rcmail.command){
parent.rcmail.command(_44,_45);
}
return false;
}
if(this.task=="mail"&&this.env.action=="compose"&&(_44=="list"||_44=="mail"||_44=="addressbook"||_44=="settings")){
if(this.cmp_hash!=this.compose_field_hash()&&!confirm(this.get_label("notsentwarning"))){
return false;
}
}
if(typeof this.command_handlers[_44]=="function"){
var ret=this.command_handlers[_44](_45,obj);
return ret!==null?ret:(obj?false:true);
}else{
if(typeof this.command_handlers[_44]=="string"){
var ret=window[this.command_handlers[_44]](_45,obj);
return ret!==null?ret:(obj?false:true);
}
}
var _48=this.triggerEvent("before"+_44,_45);
if(typeof _48!="undefined"){
if(_48===false){
return false;
}else{
_45=_48;
}
}
switch(_44){
case "login":
if(this.gui_objects.loginform){
this.gui_objects.loginform.submit();
}
break;
case "mail":
case "addressbook":
case "settings":
case "logout":
this.switch_task(_44);
break;
case "permaurl":
if(obj&&obj.href&&obj.target){
return true;
}else{
if(this.env.permaurl){
parent.location.href=this.env.permaurl;
}
}
break;
case "open":
var uid;
if(uid=this.get_single_uid()){
obj.href="?_task="+this.env.task+"&_action=show&_mbox="+urlencode(this.env.mailbox)+"&_uid="+uid;
return true;
}
break;
case "list":
if(this.task=="mail"){
if(this.env.search_request<0||(_45!=""&&(this.env.search_request&&_45!=this.env.mailbox))){
this.reset_qsearch();
}
this.list_mailbox(_45);
if(this.env.trash_mailbox){
this.set_alttext("delete",this.env.mailbox!=this.env.trash_mailbox?"movemessagetotrash":"deletemessage");
}
}else{
if(this.task=="addressbook"){
if(this.env.search_request<0||(this.env.search_request&&_45!=this.env.source)){
this.reset_qsearch();
}
this.list_contacts(_45);
this.enable_command("add",(this.env.address_sources&&!this.env.address_sources[_45].readonly));
}
}
break;
case "load-headers":
this.load_headers(obj);
break;
case "sort":
var _4a,_4b=_45;
if(this.env.sort_col==_4b){
_4a=this.env.sort_order=="ASC"?"DESC":"ASC";
}else{
_4a="ASC";
}
$("#rcm"+this.env.sort_col).removeClass("sorted"+(this.env.sort_order.toUpperCase()));
$("#rcm"+_4b).addClass("sorted"+_4a);
this.env.sort_col=_4b;
this.env.sort_order=_4a;
this.list_mailbox("","",_4b+"_"+_4a);
break;
case "nextpage":
this.list_page("next");
break;
case "lastpage":
this.list_page("last");
break;
case "previouspage":
this.list_page("prev");
break;
case "firstpage":
this.list_page("first");
break;
case "expunge":
if(this.env.messagecount){
this.expunge_mailbox(this.env.mailbox);
}
break;
case "purge":
case "empty-mailbox":
if(this.env.messagecount){
this.purge_mailbox(this.env.mailbox);
}
break;
case "show":
if(this.task=="mail"){
var uid=this.get_single_uid();
if(uid&&(!this.env.uid||uid!=this.env.uid)){
if(this.env.mailbox==this.env.drafts_mailbox){
this.goto_url("compose","_draft_uid="+uid+"&_mbox="+urlencode(this.env.mailbox),true);
}else{
this.show_message(uid);
}
}
}else{
if(this.task=="addressbook"){
var cid=_45?_45:this.get_single_cid();
if(cid&&!(this.env.action=="show"&&cid==this.env.cid)){
this.load_contact(cid,"show");
}
}
}
break;
case "add":
if(this.task=="addressbook"){
this.load_contact(0,"add");
}else{
if(this.task=="settings"){
this.identity_list.clear_selection();
this.load_identity(0,"add-identity");
}
}
break;
case "edit":
var cid;
if(this.task=="addressbook"&&(cid=this.get_single_cid())){
this.load_contact(cid,"edit");
}else{
if(this.task=="settings"&&_45){
this.load_identity(_45,"edit-identity");
}else{
if(this.task=="mail"&&(cid=this.get_single_uid())){
var url=(this.env.mailbox==this.env.drafts_mailbox)?"_draft_uid=":"_uid=";
this.goto_url("compose",url+cid+"&_mbox="+urlencode(this.env.mailbox),true);
}
}
}
break;
case "save-identity":
case "save":
if(this.gui_objects.editform){
var _4e=$("input[name='_pagesize']");
var _4f=$("input[name='_name']");
var _50=$("input[name='_email']");
if(_4e.length&&isNaN(parseInt(_4e.val()))){
alert(this.get_label("nopagesizewarning"));
_4e.focus();
break;
}else{
if(_4f.length&&_4f.val()==""){
alert(this.get_label("nonamewarning"));
_4f.focus();
break;
}else{
if(_50.length&&!rcube_check_email(_50.val())){
alert(this.get_label("noemailwarning"));
_50.focus();
break;
}
}
}
this.gui_objects.editform.submit();
}
break;
case "delete":
if(this.task=="mail"){
this.delete_messages();
}else{
if(this.task=="addressbook"){
this.delete_contacts();
}else{
if(this.task=="settings"){
this.delete_identity();
}
}
}
break;
case "move":
case "moveto":
if(this.task=="mail"){
this.move_messages(_45);
}else{
if(this.task=="addressbook"&&this.drag_active){
this.copy_contact(null,_45);
}
}
break;
case "mark":
if(_45){
this.mark_message(_45);
}
break;
case "toggle_status":
if(_45&&!_45._row){
break;
}
var uid;
var _51="read";
if(_45._row.uid){
uid=_45._row.uid;
if(this.message_list.rows[uid].deleted){
_51="undelete";
}else{
if(!this.message_list.rows[uid].unread){
_51="unread";
}
}
}
this.mark_message(_51,uid);
break;
case "toggle_flag":
if(_45&&!_45._row){
break;
}
var uid;
var _51="flagged";
if(_45._row.uid){
uid=_45._row.uid;
if(this.message_list.rows[uid].flagged){
_51="unflagged";
}
}
this.mark_message(_51,uid);
break;
case "always-load":
if(this.env.uid&&this.env.sender){
this.add_contact(urlencode(this.env.sender));
window.setTimeout(function(){
_1.command("load-images");
},300);
break;
}
case "load-images":
if(this.env.uid){
this.show_message(this.env.uid,true,this.env.action=="preview");
}
break;
case "load-attachment":
var _52="_mbox="+urlencode(this.env.mailbox)+"&_uid="+this.env.uid+"&_part="+_45.part;
if(this.env.uid&&_45.mimetype&&find_in_array(_45.mimetype,this.mimetypes)>=0){
if(_45.mimetype=="text/html"){
_52+="&_safe=1";
}
this.attachment_win=window.open(this.env.comm_path+"&_action=get&"+_52+"&_frame=1","rcubemailattachment");
if(this.attachment_win){
window.setTimeout(function(){
_1.attachment_win.focus();
},10);
break;
}
}
this.goto_url("get",_52+"&_download=1",false);
break;
case "select-all":
if(_45=="invert"){
this.message_list.invert_selection();
}else{
this.message_list.select_all(_45);
}
break;
case "select-none":
this.message_list.clear_selection();
break;
case "nextmessage":
if(this.env.next_uid){
this.show_message(this.env.next_uid,false,this.env.action=="preview");
}
break;
case "lastmessage":
if(this.env.last_uid){
this.show_message(this.env.last_uid);
}
break;
case "previousmessage":
if(this.env.prev_uid){
this.show_message(this.env.prev_uid,false,this.env.action=="preview");
}
break;
case "firstmessage":
if(this.env.first_uid){
this.show_message(this.env.first_uid);
}
break;
case "checkmail":
this.check_for_recent(true);
break;
case "compose":
var url=this.env.comm_path+"&_action=compose";
if(this.task=="mail"){
url+="&_mbox="+urlencode(this.env.mailbox);
if(this.env.mailbox==this.env.drafts_mailbox){
var uid;
if(uid=this.get_single_uid()){
url+="&_draft_uid="+uid;
}
}else{
if(_45){
url+="&_to="+urlencode(_45);
}
}
}else{
if(this.task=="addressbook"){
if(_45&&_45.indexOf("@")>0){
url=this.get_task_url("mail",url);
this.redirect(url+"&_to="+urlencode(_45));
break;
}
var _53=new Array();
if(_45){
_53[_53.length]=_45;
}else{
if(this.contact_list){
var _54=this.contact_list.get_selection();
for(var n=0;n<_54.length;n++){
_53[_53.length]=_54[n];
}
}
}
if(_53.length){
this.http_request("mailto","_cid="+urlencode(_53.join(","))+"&_source="+urlencode(this.env.source),true);
}
break;
}
}
url=url.replace(/&_framed=1/,"");
this.redirect(url);
break;
case "spellcheck":
if(window.tinyMCE&&tinyMCE.get(this.env.composebody)){
tinyMCE.execCommand("mceSpellCheck",true);
}else{
if(this.env.spellcheck&&this.env.spellcheck.spellCheck&&this.spellcheck_ready){
this.env.spellcheck.spellCheck();
this.set_spellcheck_state("checking");
}
}
break;
case "savedraft":
self.clearTimeout(this.save_timer);
if(!this.gui_objects.messageform){
break;
}
if(!this.env.drafts_mailbox||this.cmp_hash==this.compose_field_hash()){
break;
}
this.set_busy(true,"savingmessage");
var _56=this.gui_objects.messageform;
_56.target="savetarget";
_56._draft.value="1";
_56.submit();
break;
case "send":
if(!this.gui_objects.messageform){
break;
}
if(!this.check_compose_input()){
break;
}
self.clearTimeout(this.save_timer);
this.set_busy(true,"sendingmessage");
var _56=this.gui_objects.messageform;
_56.target="savetarget";
_56._draft.value="";
_56.submit();
clearTimeout(this.request_timer);
break;
case "add-attachment":
this.show_attachment_form(true);
case "send-attachment":
self.clearTimeout(this.save_timer);
this.upload_file(_45);
break;
case "remove-attachment":
this.remove_attachment(_45);
break;
case "reply-all":
case "reply":
var uid;
if(uid=this.get_single_uid()){
this.goto_url("compose","_reply_uid="+uid+"&_mbox="+urlencode(this.env.mailbox)+(_44=="reply-all"?"&_all=1":""),true);
}
break;
case "forward":
var uid;
if(uid=this.get_single_uid()){
this.goto_url("compose","_forward_uid="+uid+"&_mbox="+urlencode(this.env.mailbox),true);
}
break;
case "print":
var uid;
if(uid=this.get_single_uid()){
_1.printwin=window.open(this.env.comm_path+"&_action=print&_uid="+uid+"&_mbox="+urlencode(this.env.mailbox)+(this.env.safemode?"&_safe=1":""));
if(this.printwin){
window.setTimeout(function(){
_1.printwin.focus();
},20);
if(this.env.action!="show"){
this.mark_message("read",uid);
}
}
}
break;
case "viewsource":
var uid;
if(uid=this.get_single_uid()){
_1.sourcewin=window.open(this.env.comm_path+"&_action=viewsource&_uid="+uid+"&_mbox="+urlencode(this.env.mailbox));
if(this.sourcewin){
window.setTimeout(function(){
_1.sourcewin.focus();
},20);
}
}
break;
case "download":
var uid;
if(uid=this.get_single_uid()){
this.goto_url("viewsource","&_uid="+uid+"&_mbox="+urlencode(this.env.mailbox)+"&_save=1");
}
break;
case "add-contact":
this.add_contact(_45);
break;
case "search":
if(!_45&&this.gui_objects.qsearchbox){
_45=this.gui_objects.qsearchbox.value;
}
if(_45){
this.qsearch(_45);
break;
}
case "reset-search":
var s=this.env.search_request;
this.reset_qsearch();
if(s&&this.env.mailbox){
this.list_mailbox(this.env.mailbox);
}else{
if(s&&this.task=="addressbook"){
this.list_contacts(this.env.source);
}
}
break;
case "import":
if(this.env.action=="import"&&this.gui_objects.importform){
var _58=document.getElementById("rcmimportfile");
if(_58&&!_58.value){
alert(this.get_label("selectimportfile"));
break;
}
this.gui_objects.importform.submit();
this.set_busy(true,"importwait");
this.lock_form(this.gui_objects.importform,true);
}else{
this.goto_url("import");
}
break;
case "export":
if(this.contact_list.rowcount>0){
var _59=(this.env.source?"_source="+urlencode(this.env.source)+"&":"");
if(this.env.search_request){
_59+="_search="+this.env.search_request;
}
this.goto_url("export",_59);
}
break;
case "collapse-folder":
if(_45){
this.collapse_folder(_45);
}
break;
case "preferences":
this.goto_url("");
break;
case "identities":
this.goto_url("identities");
break;
case "delete-identity":
this.delete_identity();
case "folders":
this.goto_url("folders");
break;
case "subscribe":
this.subscribe_folder(_45);
break;
case "unsubscribe":
this.unsubscribe_folder(_45);
break;
case "create-folder":
this.create_folder(_45);
break;
case "rename-folder":
this.rename_folder(_45);
break;
case "delete-folder":
this.delete_folder(_45);
break;
}
this.triggerEvent("after"+_44,_45);
return obj?false:true;
};
this.enable_command=function(){
var _5a=arguments;
if(!_5a.length){
return -1;
}
var _5b;
var _5c=_5a[_5a.length-1];
for(var n=0;n<_5a.length-1;n++){
_5b=_5a[n];
this.commands[_5b]=_5c;
this.set_button(_5b,(_5c?"act":"pas"));
}
return true;
};
this.set_busy=function(a,_5f){
if(a&&_5f){
var msg=this.get_label(_5f);
if(msg==_5f){
msg="Loading...";
}
this.display_message(msg,"loading",true);
}else{
if(!a){
this.hide_message();
}
}
this.busy=a;
if(this.gui_objects.editform){
this.lock_form(this.gui_objects.editform,a);
}
if(this.request_timer){
clearTimeout(this.request_timer);
}
if(a&&this.env.request_timeout){
this.request_timer=window.setTimeout(function(){
_1.request_timed_out();
},this.env.request_timeout*1000);
}
};
this.get_label=function(_61,_62){
if(_62&&this.labels[_62+"."+_61]){
return this.labels[_62+"."+_61];
}else{
if(this.labels[_61]){
return this.labels[_61];
}else{
return _61;
}
}
};
this.gettext=this.get_label;
this.switch_task=function(_63){
if(this.task===_63&&_63!="mail"){
return;
}
var url=this.get_task_url(_63);
if(_63=="mail"){
url+="&_mbox=INBOX";
}
this.redirect(url);
};
this.get_task_url=function(_65,url){
if(!url){
url=this.env.comm_path;
}
return url.replace(/_task=[a-z]+/,"_task="+_65);
};
this.request_timed_out=function(){
this.set_busy(false);
this.display_message("Request timed out!","error");
};
this.reload=function(_67){
if(this.env.framed&&parent.rcmail){
parent.rcmail.reload(_67);
}else{
if(_67){
window.setTimeout(function(){
rcmail.reload();
},_67);
}else{
if(window.location){
location.href=this.env.comm_path;
}
}
}
};
this.doc_mouse_up=function(e){
var _69,_6a,li;
if(this.message_list){
if(!rcube_mouse_is_over(e,this.message_list.list)){
this.message_list.blur();
}
_6a=this.message_list;
_69=this.env.mailboxes;
}else{
if(this.contact_list){
if(!rcube_mouse_is_over(e,this.contact_list.list)){
this.contact_list.blur();
}
_6a=this.contact_list;
_69=this.env.address_sources;
}else{
if(this.ksearch_value){
this.ksearch_blur();
}
}
}
if(this.drag_active&&_69&&this.env.last_folder_target){
$(this.get_folder_li(this.env.last_folder_target)).removeClass("droptarget");
this.command("moveto",_69[this.env.last_folder_target].id);
this.env.last_folder_target=null;
_6a.draglayer.hide();
}
if(this.buttons_sel){
for(var id in this.buttons_sel){
if(typeof id!="function"){
this.button_out(this.buttons_sel[id],id);
}
}
this.buttons_sel={};
}
};
this.drag_start=function(_6d){
var _6e=this.task=="mail"?this.env.mailboxes:this.env.address_sources;
this.drag_active=true;
if(this.preview_timer){
clearTimeout(this.preview_timer);
}
if(this.gui_objects.folderlist&&_6e){
this.initialBodyScrollTop=bw.ie?0:window.pageYOffset;
this.initialListScrollTop=this.gui_objects.folderlist.parentNode.scrollTop;
var li,pos,_6d,_71;
_6d=$(this.gui_objects.folderlist);
pos=_6d.offset();
this.env.folderlist_coords={x1:pos.left,y1:pos.top,x2:pos.left+_6d.width(),y2:pos.top+_6d.height()};
this.env.folder_coords=new Array();
for(var k in _6e){
if(li=this.get_folder_li(k)){
if(_71=li.firstChild.offsetHeight){
pos=$(li.firstChild).offset();
this.env.folder_coords[k]={x1:pos.left,y1:pos.top,x2:pos.left+li.firstChild.offsetWidth,y2:pos.top+_71,on:0};
}
}
}
}
};
this.drag_end=function(e){
this.drag_active=false;
this.env.last_folder_target=null;
if(this.folder_auto_timer){
window.clearTimeout(this.folder_auto_timer);
this.folder_auto_timer=null;
this.folder_auto_expand=null;
}
if(this.gui_objects.folderlist&&this.env.folder_coords){
for(var k in this.env.folder_coords){
if(this.env.folder_coords[k].on){
$(this.get_folder_li(k)).removeClass("droptarget");
}
}
}
};
this.drag_move=function(e){
if(this.gui_objects.folderlist&&this.env.folder_coords){
var _76=bw.ie?-document.documentElement.scrollTop:this.initialBodyScrollTop;
var _77=this.initialListScrollTop-this.gui_objects.folderlist.parentNode.scrollTop;
var _78=-_77-_76;
var li,div,pos,_7c;
_7c=rcube_event.get_mouse_pos(e);
pos=this.env.folderlist_coords;
_7c.y+=_78;
if(_7c.x<pos.x1||_7c.x>=pos.x2||_7c.y<pos.y1||_7c.y>=pos.y2){
if(this.env.last_folder_target){
$(this.get_folder_li(this.env.last_folder_target)).removeClass("droptarget");
this.env.folder_coords[this.env.last_folder_target].on=0;
this.env.last_folder_target=null;
}
return;
}
for(var k in this.env.folder_coords){
pos=this.env.folder_coords[k];
if(_7c.x>=pos.x1&&_7c.x<pos.x2&&_7c.y>=pos.y1&&_7c.y<pos.y2&&this.check_droptarget(k)){
li=this.get_folder_li(k);
div=$(li.getElementsByTagName("div")[0]);
if(div.hasClass("collapsed")){
if(this.folder_auto_timer){
window.clearTimeout(this.folder_auto_timer);
}
this.folder_auto_expand=k;
this.folder_auto_timer=window.setTimeout(function(){
rcmail.command("collapse-folder",rcmail.folder_auto_expand);
rcmail.drag_start(null);
},1000);
}else{
if(this.folder_auto_timer){
window.clearTimeout(this.folder_auto_timer);
this.folder_auto_timer=null;
this.folder_auto_expand=null;
}
}
$(li).addClass("droptarget");
this.env.last_folder_target=k;
this.env.folder_coords[k].on=1;
}else{
if(pos.on){
$(this.get_folder_li(k)).removeClass("droptarget");
this.env.folder_coords[k].on=0;
}
}
}
}
};
this.collapse_folder=function(id){
var div;
if((li=this.get_folder_li(id))&&(div=$(li.getElementsByTagName("div")[0]))&&(div.hasClass("collapsed")||div.hasClass("expanded"))){
var ul=$(li.getElementsByTagName("ul")[0]);
if(div.hasClass("collapsed")){
ul.show();
div.removeClass("collapsed").addClass("expanded");
var reg=new RegExp("&"+urlencode(id)+"&");
this.set_env("collapsed_folders",this.env.collapsed_folders.replace(reg,""));
}else{
ul.hide();
div.removeClass("expanded").addClass("collapsed");
this.set_env("collapsed_folders",this.env.collapsed_folders+"&"+urlencode(id)+"&");
if(this.env.mailbox.indexOf(id+this.env.delimiter)==0){
this.command("list",id);
}
}
if((bw.ie6||bw.ie7)&&li.nextSibling&&(li.nextSibling.getElementsByTagName("ul").length>0)&&li.nextSibling.getElementsByTagName("ul")[0].style&&(li.nextSibling.getElementsByTagName("ul")[0].style.display!="none")){
li.nextSibling.getElementsByTagName("ul")[0].style.display="none";
li.nextSibling.getElementsByTagName("ul")[0].style.display="";
}
this.http_post("save-pref","_name=collapsed_folders&_value="+urlencode(this.env.collapsed_folders));
this.set_unread_count_display(id,false);
}
};
this.click_on_list=function(e){
if(this.gui_objects.qsearchbox){
this.gui_objects.qsearchbox.blur();
}
if(this.message_list){
this.message_list.focus();
}else{
if(this.contact_list){
this.contact_list.focus();
}
}
return rcube_event.get_button(e)==2?true:rcube_event.cancel(e);
};
this.msglist_select=function(_83){
if(this.preview_timer){
clearTimeout(this.preview_timer);
}
var _84=_83.selection.length==1;
if(this.env.mailbox==this.env.drafts_mailbox){
this.enable_command("reply","reply-all","forward",false);
this.enable_command("show","print","open","edit","download","viewsource",_84);
this.enable_command("delete","moveto","mark",(_83.selection.length>0?true:false));
}else{
this.enable_command("show","reply","reply-all","forward","print","edit","open","download","viewsource",_84);
this.enable_command("delete","moveto","mark",(_83.selection.length>0?true:false));
}
if(_84&&this.env.contentframe&&!_83.multi_selecting){
this.preview_timer=window.setTimeout(function(){
_1.msglist_get_preview();
},200);
}else{
if(this.env.contentframe){
this.show_contentframe(false);
}
}
};
this.msglist_dbl_click=function(_85){
if(this.preview_timer){
clearTimeout(this.preview_timer);
}
var uid=_85.get_single_selection();
if(uid&&this.env.mailbox==this.env.drafts_mailbox){
this.goto_url("compose","_draft_uid="+uid+"&_mbox="+urlencode(this.env.mailbox),true);
}else{
if(uid){
this.show_message(uid,false,false);
}
}
};
this.msglist_keypress=function(_87){
if(_87.key_pressed==_87.ENTER_KEY){
this.command("show");
}else{
if(_87.key_pressed==_87.DELETE_KEY){
this.command("delete");
}else{
if(_87.key_pressed==_87.BACKSPACE_KEY){
this.command("delete");
}else{
_87.shiftkey=false;
}
}
}
};
this.msglist_get_preview=function(){
var uid=this.get_single_uid();
if(uid&&this.env.contentframe&&!this.drag_active){
this.show_message(uid,false,true);
}else{
if(this.env.contentframe){
this.show_contentframe(false);
}
}
};
this.check_droptarget=function(id){
if(this.task=="mail"){
return (this.env.mailboxes[id]&&this.env.mailboxes[id].id!=this.env.mailbox&&!this.env.mailboxes[id].virtual);
}else{
if(this.task=="addressbook"){
return (id!=this.env.source&&this.env.address_sources[id]&&!this.env.address_sources[id].readonly);
}else{
if(this.task=="settings"){
return (id!=this.env.folder);
}
}
}
};
this.show_message=function(id,_8b,_8c){
if(!id){
return;
}
var _8d="";
var _8e=_8c?"preview":"show";
var _8f=window;
if(_8c&&this.env.contentframe&&window.frames&&window.frames[this.env.contentframe]){
_8f=window.frames[this.env.contentframe];
_8d="&_framed=1";
}
if(_8b){
_8d="&_safe=1";
}
if(this.env.search_request){
_8d+="&_search="+this.env.search_request;
}
var url="&_action="+_8e+"&_uid="+id+"&_mbox="+urlencode(this.env.mailbox)+_8d;
if(_8e=="preview"&&String(_8f.location.href).indexOf(url)>=0){
this.show_contentframe(true);
}else{
this.set_busy(true,"loading");
_8f.location.href=this.env.comm_path+url;
if(_8e=="preview"&&this.message_list&&this.message_list.rows[id]&&this.message_list.rows[id].unread){
this.set_message(id,"unread",false);
if(this.env.unread_counts[this.env.mailbox]){
this.env.unread_counts[this.env.mailbox]-=1;
this.set_unread_count(this.env.mailbox,this.env.unread_counts[this.env.mailbox],this.env.mailbox=="INBOX");
}
}
}
};
this.show_contentframe=function(_91){
var frm;
if(this.env.contentframe&&(frm=$("#"+this.env.contentframe))&&frm.length){
if(!_91&&window.frames[this.env.contentframe]){
if(window.frames[this.env.contentframe].location.href.indexOf(this.env.blankpage)<0){
window.frames[this.env.contentframe].location.href=this.env.blankpage;
}
}else{
if(!bw.safari&&!bw.konq){
frm[_91?"show":"hide"]();
}
}
}
if(!_91&&this.busy){
this.set_busy(false);
}
};
this.list_page=function(_93){
if(_93=="next"){
_93=this.env.current_page+1;
}
if(_93=="last"){
_93=this.env.pagecount;
}
if(_93=="prev"&&this.env.current_page>1){
_93=this.env.current_page-1;
}
if(_93=="first"&&this.env.current_page>1){
_93=1;
}
if(_93>0&&_93<=this.env.pagecount){
this.env.current_page=_93;
if(this.task=="mail"){
this.list_mailbox(this.env.mailbox,_93);
}else{
if(this.task=="addressbook"){
this.list_contacts(this.env.source,_93);
}
}
}
};
this.filter_mailbox=function(_94){
var _95;
if(this.gui_objects.qsearchbox){
_95=this.gui_objects.qsearchbox.value;
}
this.message_list.clear();
this.env.current_page=1;
this.set_busy(true,"searching");
this.http_request("search","_filter="+_94+(_95?"&_q="+urlencode(_95):"")+(this.env.mailbox?"&_mbox="+urlencode(this.env.mailbox):""),true);
};
this.list_mailbox=function(_96,_97,_98){
var _99="";
var _9a=window;
if(!_96){
_96=this.env.mailbox;
}
if(_98){
_99+="&_sort="+_98;
}
if(this.env.search_request){
_99+="&_search="+this.env.search_request;
}
if(!_97){
_97=1;
this.env.current_page=_97;
this.show_contentframe(false);
}
if(_96!=this.env.mailbox||(_96==this.env.mailbox&&!_97&&!_98)){
_99+="&_refresh=1";
}
this.last_selected=0;
if(this.message_list){
this.message_list.clear_selection();
}
this.select_folder(_96,this.env.mailbox);
this.env.mailbox=_96;
if(this.gui_objects.messagelist){
this.list_mailbox_remote(_96,_97,_99);
return;
}
if(this.env.contentframe&&window.frames&&window.frames[this.env.contentframe]){
_9a=window.frames[this.env.contentframe];
_99+="&_framed=1";
}
if(_96){
this.set_busy(true,"loading");
_9a.location.href=this.env.comm_path+"&_mbox="+urlencode(_96)+(_97?"&_page="+_97:"")+_99;
}
};
this.list_mailbox_remote=function(_9b,_9c,_9d){
this.message_list.clear();
var url="_mbox="+urlencode(_9b)+(_9c?"&_page="+_9c:"");
this.set_busy(true,"loading");
this.http_request("list",url+_9d,true);
};
this.expunge_mailbox=function(_9f){
var _a0=false;
var _a1="";
if(_9f==this.env.mailbox){
_a0=true;
this.set_busy(true,"loading");
_a1="&_reload=1";
}
var url="_mbox="+urlencode(_9f);
this.http_post("expunge",url+_a1,_a0);
};
this.purge_mailbox=function(_a3){
var _a4=false;
var _a5="";
if(!confirm(this.get_label("purgefolderconfirm"))){
return false;
}
if(_a3==this.env.mailbox){
_a4=true;
this.set_busy(true,"loading");
_a5="&_reload=1";
}
var url="_mbox="+urlencode(_a3);
this.http_post("purge",url+_a5,_a4);
return true;
};
this.purge_mailbox_test=function(){
return (this.env.messagecount&&(this.env.mailbox==this.env.trash_mailbox||this.env.mailbox==this.env.junk_mailbox||this.env.mailbox.match("^"+RegExp.escape(this.env.trash_mailbox)+RegExp.escape(this.env.delimiter))||this.env.mailbox.match("^"+RegExp.escape(this.env.junk_mailbox)+RegExp.escape(this.env.delimiter))));
};
this.set_message_icon=function(uid){
var _a8;
var _a9=this.message_list.rows;
if(!_a9[uid]){
return false;
}
if(_a9[uid].deleted&&this.env.deletedicon){
_a8=this.env.deletedicon;
}else{
if(_a9[uid].replied&&this.env.repliedicon){
if(_a9[uid].forwarded&&this.env.forwardedrepliedicon){
_a8=this.env.forwardedrepliedicon;
}else{
_a8=this.env.repliedicon;
}
}else{
if(_a9[uid].forwarded&&this.env.forwardedicon){
_a8=this.env.forwardedicon;
}else{
if(_a9[uid].unread&&this.env.unreadicon){
_a8=this.env.unreadicon;
}else{
if(this.env.messageicon){
_a8=this.env.messageicon;
}
}
}
}
}
if(_a8&&_a9[uid].icon){
_a9[uid].icon.src=_a8;
}
_a8="";
if(_a9[uid].flagged&&this.env.flaggedicon){
_a8=this.env.flaggedicon;
}else{
if(!_a9[uid].flagged&&this.env.unflaggedicon){
_a8=this.env.unflaggedicon;
}
}
if(_a9[uid].flagged_icon&&_a8){
_a9[uid].flagged_icon.src=_a8;
}
};
this.set_message_status=function(uid,_ab,_ac){
var _ad=this.message_list.rows;
if(!_ad[uid]){
return false;
}
if(_ab=="unread"){
_ad[uid].unread=_ac;
}else{
if(_ab=="deleted"){
_ad[uid].deleted=_ac;
}else{
if(_ab=="replied"){
_ad[uid].replied=_ac;
}else{
if(_ab=="forwarded"){
_ad[uid].forwarded=_ac;
}else{
if(_ab=="flagged"){
_ad[uid].flagged=_ac;
}
}
}
}
}
this.env.messages[uid]=_ad[uid];
};
this.set_message=function(uid,_af,_b0){
var _b1=this.message_list.rows;
if(!_b1[uid]){
return false;
}
if(_af){
this.set_message_status(uid,_af,_b0);
}
var _b2=$(_b1[uid].obj);
if(_b1[uid].unread&&_b1[uid].classname.indexOf("unread")<0){
_b1[uid].classname+=" unread";
_b2.addClass("unread");
}else{
if(!_b1[uid].unread&&_b1[uid].classname.indexOf("unread")>=0){
_b1[uid].classname=_b1[uid].classname.replace(/\s*unread/,"");
_b2.removeClass("unread");
}
}
if(_b1[uid].deleted&&_b1[uid].classname.indexOf("deleted")<0){
_b1[uid].classname+=" deleted";
_b2.addClass("deleted");
}else{
if(!_b1[uid].deleted&&_b1[uid].classname.indexOf("deleted")>=0){
_b1[uid].classname=_b1[uid].classname.replace(/\s*deleted/,"");
_b2.removeClass("deleted");
}
}
if(_b1[uid].flagged&&_b1[uid].classname.indexOf("flagged")<0){
_b1[uid].classname+=" flagged";
_b2.addClass("flagged");
}else{
if(!_b1[uid].flagged&&_b1[uid].classname.indexOf("flagged")>=0){
_b1[uid].classname=_b1[uid].classname.replace(/\s*flagged/,"");
_b2.removeClass("flagged");
}
}
this.set_message_icon(uid);
};
this.move_messages=function(_b3){
if(!_b3||_b3==this.env.mailbox||(!this.env.uid&&(!this.message_list||!this.message_list.get_selection().length))){
return;
}
var _b4=false;
var _b5="&_target_mbox="+urlencode(_b3)+"&_from="+(this.env.action?this.env.action:"");
if(this.env.action=="show"){
_b4=true;
this.set_busy(true,"movingmessage");
}else{
this.show_contentframe(false);
}
this.enable_command("reply","reply-all","forward","delete","mark","print","open","edit","viewsource","download",false);
this._with_selected_messages("moveto",_b4,_b5);
};
this.delete_messages=function(){
var _b6=this.message_list?this.message_list.get_selection():new Array();
if(!this.env.uid&&!_b6.length){
return;
}
if(this.env.flag_for_deletion){
this.mark_message("delete");
}else{
if(!this.env.trash_mailbox||String(this.env.mailbox).toLowerCase()==String(this.env.trash_mailbox).toLowerCase()){
this.permanently_remove_messages();
}else{
if(this.message_list&&this.message_list.shiftkey){
if(confirm(this.get_label("deletemessagesconfirm"))){
this.permanently_remove_messages();
}
}else{
this.move_messages(this.env.trash_mailbox);
}
}
}
};
this.permanently_remove_messages=function(){
if(!this.env.uid&&(!this.message_list||!this.message_list.get_selection().length)){
return;
}
this.show_contentframe(false);
this._with_selected_messages("delete",false,"&_from="+(this.env.action?this.env.action:""));
};
this._with_selected_messages=function(_b7,_b8,_b9,_ba){
var _bb=new Array();
if(this.env.uid){
_bb[0]=this.env.uid;
}else{
var _bc=this.message_list.get_selection();
var _bd=this.message_list.rows;
var id;
for(var n=0;n<_bc.length;n++){
id=_bc[n];
_bb[_bb.length]=id;
this.message_list.remove_row(id,(this.env.display_next&&n==_bc.length-1));
}
if(!this.env.display_next){
this.message_list.clear_selection();
}
}
if(this.env.search_request){
_b9+="&_search="+this.env.search_request;
}
if(this.env.display_next&&this.env.next_uid){
_b9+="&_next_uid="+this.env.next_uid;
}
this.http_post(_b7,"_uid="+_bb.join(",")+"&_mbox="+urlencode(this.env.mailbox)+_b9,_b8);
};
this.mark_message=function(_c0,uid){
var _c2=new Array();
var _c3=new Array();
var _c4=this.message_list?this.message_list.get_selection():new Array();
if(uid){
_c2[0]=uid;
}else{
if(this.env.uid){
_c2[0]=this.env.uid;
}else{
if(this.message_list){
for(var n=0;n<_c4.length;n++){
_c2[_c2.length]=_c4[n];
}
}
}
}
if(!this.message_list){
_c3=_c2;
}else{
for(var id,n=0;n<_c2.length;n++){
id=_c2[n];
if((_c0=="read"&&this.message_list.rows[id].unread)||(_c0=="unread"&&!this.message_list.rows[id].unread)||(_c0=="delete"&&!this.message_list.rows[id].deleted)||(_c0=="undelete"&&this.message_list.rows[id].deleted)||(_c0=="flagged"&&!this.message_list.rows[id].flagged)||(_c0=="unflagged"&&this.message_list.rows[id].flagged)){
_c3[_c3.length]=id;
}
}
}
if(!_c3.length){
return;
}
switch(_c0){
case "read":
case "unread":
this.toggle_read_status(_c0,_c3);
break;
case "delete":
case "undelete":
this.toggle_delete_status(_c3);
break;
case "flagged":
case "unflagged":
this.toggle_flagged_status(_c0,_c2);
break;
}
};
this.toggle_read_status=function(_c7,_c8){
for(var i=0;i<_c8.length;i++){
this.set_message(_c8[i],"unread",(_c7=="unread"?true:false));
}
this.http_post("mark","_uid="+_c8.join(",")+"&_flag="+_c7);
};
this.toggle_flagged_status=function(_ca,_cb){
for(var i=0;i<_cb.length;i++){
this.set_message(_cb[i],"flagged",(_ca=="flagged"?true:false));
}
this.http_post("mark","_uid="+_cb.join(",")+"&_flag="+_ca);
};
this.toggle_delete_status=function(_cd){
var _ce=this.message_list?this.message_list.rows:new Array();
if(_cd.length==1){
if(!_ce.length||(_ce[_cd[0]]&&!_ce[_cd[0]].deleted)){
this.flag_as_deleted(_cd);
}else{
this.flag_as_undeleted(_cd);
}
return true;
}
var _cf=true;
for(var i=0;i<_cd.length;i++){
uid=_cd[i];
if(_ce[uid]){
if(!_ce[uid].deleted){
_cf=false;
break;
}
}
}
if(_cf){
this.flag_as_undeleted(_cd);
}else{
this.flag_as_deleted(_cd);
}
return true;
};
this.flag_as_undeleted=function(_d1){
for(var i=0;i<_d1.length;i++){
this.set_message(_d1[i],"deleted",false);
}
this.http_post("mark","_uid="+_d1.join(",")+"&_flag=undelete");
return true;
};
this.flag_as_deleted=function(_d3){
var _d4="";
var _d5=new Array();
var _d6=this.message_list?this.message_list.rows:new Array();
for(var i=0;i<_d3.length;i++){
uid=_d3[i];
if(_d6[uid]){
if(_d6[uid].unread){
_d5[_d5.length]=uid;
}
if(this.env.skip_deleted){
this.message_list.remove_row(uid,(this.env.display_next&&i==this.message_list.selection.length-1));
}else{
this.set_message(uid,"deleted",true);
}
}
}
if(this.env.skip_deleted&&!this.env.display_next&&this.message_list){
this.message_list.clear_selection();
}
_d4="&_from="+(this.env.action?this.env.action:"");
if(_d5.length){
_d4+="&_ruid="+_d5.join(",");
}
if(this.env.skip_deleted){
if(this.env.search_request){
_d4+="&_search="+this.env.search_request;
}
if(this.env.display_next&&this.env.next_uid){
_d4+="&_next_uid="+this.env.next_uid;
}
}
this.http_post("mark","_uid="+_d3.join(",")+"&_flag=delete"+_d4);
return true;
};
this.flag_deleted_as_read=function(_d8){
var _d9;
var _da=this.message_list?this.message_list.rows:new Array();
var str=String(_d8);
var _dc=new Array();
_dc=str.split(",");
for(var uid,i=0;i<_dc.length;i++){
uid=_dc[i];
if(_da[uid]){
this.set_message(uid,"unread",false);
}
}
};
this.login_user_keyup=function(e){
var key=rcube_event.get_keycode(e);
var _e1=$("#rcmloginpwd");
if(key==13&&_e1.length&&!_e1.val()){
_e1.focus();
return rcube_event.cancel(e);
}
return true;
};
this.check_compose_input=function(){
var _e2=$("[name='_to']");
var _e3=$("[name='_cc']");
var _e4=$("[name='_bcc']");
var _e5=$("[name='_from']");
var _e6=$("[name='_subject']");
var _e7=$("[name='_message']");
if(_e5.attr("type")=="text"&&!rcube_check_email(_e5.val(),true)){
alert(this.get_label("nosenderwarning"));
_e5.focus();
return false;
}
var _e8=_e2.val()?_e2.val():(_e3.val()?_e3.val():_e4.val());
if(!rcube_check_email(_e8.replace(/^\s+/,"").replace(/[\s,;]+$/,""),true)){
alert(this.get_label("norecipientwarning"));
_e2.focus();
return false;
}
if(_e6.val()==""){
var _e9=prompt(this.get_label("nosubjectwarning"),this.get_label("nosubject"));
if(!_e9&&_e9!==""){
_e6.focus();
return false;
}else{
_e6.val((_e9?_e9:this.get_label("nosubject")));
}
}
if((!window.tinyMCE||!tinyMCE.get(this.env.composebody))&&_e7.val()==""&&!confirm(this.get_label("nobodywarning"))){
_e7.focus();
return false;
}else{
if(window.tinyMCE&&tinyMCE.get(this.env.composebody)&&!tinyMCE.get(this.env.composebody).getContent()&&!confirm(this.get_label("nobodywarning"))){
tinyMCE.get(this.env.composebody).focus();
return false;
}
}
this.stop_spellchecking();
if(window.tinyMCE&&tinyMCE.get(this.env.composebody)){
tinyMCE.triggerSave();
}
return true;
};
this.stop_spellchecking=function(){
if(this.env.spellcheck&&!this.spellcheck_ready){
$(this.env.spellcheck.spell_span).trigger("click");
this.set_spellcheck_state("ready");
}
};
this.display_spellcheck_controls=function(vis){
if(this.env.spellcheck){
if(!vis){
this.stop_spellchecking();
}
$(this.env.spellcheck.spell_container).css("visibility",vis?"visible":"hidden");
}
};
this.set_spellcheck_state=function(s){
this.spellcheck_ready=(s=="ready"||s=="no_error_found");
this.enable_command("spellcheck",this.spellcheck_ready);
};
this.set_draft_id=function(id){
$("input[name='_draft_saveid']").val(id);
};
this.auto_save_start=function(){
if(this.env.draft_autosave){
this.save_timer=self.setTimeout(function(){
_1.command("savedraft");
},this.env.draft_autosave*1000);
}
this.busy=false;
};
this.compose_field_hash=function(_ed){
var _ee=$("[name='_to']").val();
var _ef=$("[name='_cc']").val();
var _f0=$("[name='_bcc']").val();
var _f1=$("[name='_subject']").val();
var str="";
if(_ee){
str+=_ee+":";
}
if(_ef){
str+=_ef+":";
}
if(_f0){
str+=_f0+":";
}
if(_f1){
str+=_f1+":";
}
var _f3=tinyMCE.get(this.env.composebody);
if(_f3){
str+=_f3.getContent();
}else{
str+=$("[name='_message']").val();
}
if(_ed){
this.cmp_hash=str;
}
return str;
};
this.change_identity=function(obj){
if(!obj||!obj.options){
return false;
}
var id=obj.options[obj.selectedIndex].value;
var _f6=$("[name='_message']");
var _f7=_f6.val();
var _f8=($("input[name='_is_html']").val()=="1");
var sig,p,len;
if(!this.env.identity){
this.env.identity=id;
}
if(!_f8){
if(this.env.identity&&this.env.signatures&&this.env.signatures[this.env.identity]){
if(this.env.signatures[this.env.identity]["is_html"]){
sig=this.env.signatures[this.env.identity]["plain_text"];
}else{
sig=this.env.signatures[this.env.identity]["text"];
}
if(sig.indexOf("-- ")!=0){
sig="-- \n"+sig;
}
p=_f7.lastIndexOf(sig);
if(p>=0){
_f7=_f7.substring(0,p-1)+_f7.substring(p+sig.length,_f7.length);
}
}
_f7=_f7.replace(/[\r\n]+$/,"");
len=_f7.length;
if(this.env.signatures&&this.env.signatures[id]){
sig=this.env.signatures[id]["text"];
if(this.env.signatures[id]["is_html"]){
sig=this.env.signatures[id]["plain_text"];
}
if(sig.indexOf("-- ")!=0){
sig="-- \n"+sig;
}
_f7+="\n\n"+sig;
if(len){
len+=1;
}
}
}else{
var _fc=tinyMCE.get(this.env.composebody);
if(this.env.signatures){
var _fd=_fc.dom.get("_rc_sig");
var _fe="";
var _ff=true;
if(!_fd){
if(bw.ie){
_fc.getBody().appendChild(_fc.getDoc().createElement("br"));
}
_fd=_fc.getDoc().createElement("div");
_fd.setAttribute("id","_rc_sig");
_fc.getBody().appendChild(_fd);
}
if(this.env.signatures[id]){
_fe=this.env.signatures[id]["text"];
_ff=this.env.signatures[id]["is_html"];
if(_fe){
if(_ff&&this.env.signatures[id]["plain_text"].indexOf("-- ")!=0){
_fe="<p>-- </p>"+_fe;
}else{
if(!_ff&&_fe.indexOf("-- ")!=0){
_fe="-- \n"+_fe;
}
}
}
}
if(_ff){
_fd.innerHTML=_fe;
}else{
_fd.innerHTML="<pre>"+_fe+"</pre>";
}
}
}
_f6.val(_f7);
if(!_f8){
this.set_caret_pos(_f6.get(0),len);
}
this.env.identity=id;
return true;
};
this.show_attachment_form=function(a){
if(!this.gui_objects.uploadbox){
return false;
}
var elm,list;
if(elm=this.gui_objects.uploadbox){
if(a&&(list=this.gui_objects.attachmentlist)){
var pos=$(list).offset();
elm.style.top=(pos.top+list.offsetHeight+10)+"px";
elm.style.left=pos.left+"px";
}
elm.style.visibility=a?"visible":"hidden";
}
try{
if(!a&&this.gui_objects.attachmentform!=this.gui_objects.messageform){
this.gui_objects.attachmentform.reset();
}
}
catch(e){
}
return true;
};
this.upload_file=function(form){
if(!form){
return false;
}
var send=false;
for(var n=0;n<form.elements.length;n++){
if(form.elements[n].type=="file"&&form.elements[n].value){
send=true;
break;
}
}
if(send){
var ts=new Date().getTime();
var _108="rcmupload"+ts;
if(document.all){
var html="<iframe name=\""+_108+"\" src=\"program/blank.gif\" style=\"width:0;height:0;visibility:hidden;\"></iframe>";
document.body.insertAdjacentHTML("BeforeEnd",html);
}else{
var _10a=document.createElement("iframe");
_10a.name=_108;
_10a.style.border="none";
_10a.style.width=0;
_10a.style.height=0;
_10a.style.visibility="hidden";
document.body.appendChild(_10a);
}
form.target=_108;
form.action=this.env.comm_path+"&_action=upload";
form.setAttribute("enctype","multipart/form-data");
form.submit();
}
this.gui_objects.attachmentform=form;
return true;
};
this.add2attachment_list=function(name,_10c){
if(!this.gui_objects.attachmentlist){
return false;
}
$("<li>").attr("id",name).html(_10c).appendTo(this.gui_objects.attachmentlist);
return true;
};
this.remove_from_attachment_list=function(name){
if(!this.gui_objects.attachmentlist){
return false;
}
var list=this.gui_objects.attachmentlist.getElementsByTagName("li");
for(i=0;i<list.length;i++){
if(list[i].id==name){
this.gui_objects.attachmentlist.removeChild(list[i]);
}
}
};
this.remove_attachment=function(name){
if(name){
this.http_post("remove-attachment","_file="+urlencode(name));
}
return true;
};
this.add_contact=function(_110){
if(_110){
this.http_post("addcontact","_address="+_110);
}
return true;
};
this.qsearch=function(_111){
if(_111!=""){
var _112="";
if(this.message_list){
this.message_list.clear();
if(this.env.search_mods){
var _113=new Array();
for(var n in this.env.search_mods){
_113.push(n);
}
_112+="&_headers="+_113.join(",");
}
}else{
if(this.contact_list){
this.contact_list.clear(true);
this.show_contentframe(false);
}
}
if(this.gui_objects.search_filter){
_112+="&_filter="+this.gui_objects.search_filter.value;
}
this.env.current_page=1;
this.set_busy(true,"searching");
this.http_request("search","_q="+urlencode(_111)+(this.env.mailbox?"&_mbox="+urlencode(this.env.mailbox):"")+(this.env.source?"&_source="+urlencode(this.env.source):"")+(_112?_112:""),true);
}
return true;
};
this.reset_qsearch=function(){
if(this.gui_objects.qsearchbox){
this.gui_objects.qsearchbox.value="";
}
this.env.search_request=null;
return true;
};
this.sent_successfully=function(type,msg){
this.list_mailbox();
this.display_message(msg,type,true);
};
this.ksearch_keypress=function(e,obj){
if(this.ksearch_timer){
clearTimeout(this.ksearch_timer);
}
var _119;
var key=rcube_event.get_keycode(e);
var mod=rcube_event.get_modifier(e);
switch(key){
case 38:
case 40:
if(!this.ksearch_pane){
break;
}
var dir=key==38?1:0;
_119=document.getElementById("rcmksearchSelected");
if(!_119){
_119=this.ksearch_pane.__ul.firstChild;
}
if(_119){
this.ksearch_select(dir?_119.previousSibling:_119.nextSibling);
}
return rcube_event.cancel(e);
case 9:
if(mod==SHIFT_KEY){
break;
}
case 13:
if(this.ksearch_selected===null||!this.ksearch_input||!this.ksearch_value){
break;
}
this.insert_recipient(this.ksearch_selected);
this.ksearch_hide();
return rcube_event.cancel(e);
case 27:
this.ksearch_hide();
break;
case 37:
case 39:
if(mod!=SHIFT_KEY){
return;
}
}
this.ksearch_timer=window.setTimeout(function(){
_1.ksearch_get_results();
},200);
this.ksearch_input=obj;
return true;
};
this.ksearch_select=function(node){
var _11e=$("#rcmksearchSelected");
if(_11e[0]&&node){
_11e.removeAttr("id").removeClass("selected");
}
if(node){
$(node).attr("id","rcmksearchSelected").addClass("selected");
this.ksearch_selected=node._rcm_id;
}
};
this.insert_recipient=function(id){
if(!this.env.contacts[id]||!this.ksearch_input){
return;
}
var _120=this.ksearch_input.value.toLowerCase();
var cpos=this.get_caret_pos(this.ksearch_input);
var p=_120.lastIndexOf(this.ksearch_value,cpos);
var pre=this.ksearch_input.value.substring(0,p);
var end=this.ksearch_input.value.substring(p+this.ksearch_value.length,this.ksearch_input.value.length);
var _125=this.env.contacts[id]+", ";
this.ksearch_input.value=pre+_125+end;
cpos=p+_125.length;
if(this.ksearch_input.setSelectionRange){
this.ksearch_input.setSelectionRange(cpos,cpos);
}
};
this.ksearch_get_results=function(){
var _126=this.ksearch_input?this.ksearch_input.value:null;
if(_126===null){
return;
}
if(this.ksearch_pane&&this.ksearch_pane.is(":visible")){
this.ksearch_pane.hide();
}
var cpos=this.get_caret_pos(this.ksearch_input);
var p=_126.lastIndexOf(",",cpos-1);
var q=_126.substring(p+1,cpos);
q=q.replace(/(^\s+|\s+$)/g,"").toLowerCase();
if(q==this.ksearch_value){
return;
}
var _12a=this.ksearch_value;
this.ksearch_value=q;
if(!q.length){
return;
}
if(_12a&&_12a.length&&this.env.contacts&&!this.env.contacts.length&&q.indexOf(_12a)==0){
return;
}
this.display_message(this.get_label("searching"),"loading",true);
this.http_post("autocomplete","_search="+urlencode(q));
};
this.ksearch_query_results=function(_12b,_12c){
if(this.ksearch_value&&_12c!=this.ksearch_value){
return;
}
this.hide_message();
this.env.contacts=_12b?_12b:[];
this.ksearch_display_results(this.env.contacts);
};
this.ksearch_display_results=function(_12d){
if(_12d.length&&this.ksearch_input){
var p,ul,li;
if(!this.ksearch_pane){
ul=$("<ul>");
this.ksearch_pane=$("<div>").attr("id","rcmKSearchpane").css({position:"absolute","z-index":30000}).append(ul).appendTo(document.body);
this.ksearch_pane.__ul=ul[0];
}
ul=this.ksearch_pane.__ul;
ul.innerHTML="";
for(i=0;i<_12d.length;i++){
li=document.createElement("LI");
li.innerHTML=_12d[i].replace(new RegExp("("+this.ksearch_value+")","ig"),"##$1%%").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/##([^%]+)%%/g,"<b>$1</b>");
li.onmouseover=function(){
_1.ksearch_select(this);
};
li.onmouseup=function(){
_1.ksearch_click(this);
};
li._rcm_id=i;
ul.appendChild(li);
}
$(ul.firstChild).attr("id","rcmksearchSelected").addClass("selected");
this.ksearch_selected=0;
var pos=$(this.ksearch_input).offset();
this.ksearch_pane.css({left:pos.left+"px",top:(pos.top+this.ksearch_input.offsetHeight)+"px"}).show();
}else{
this.ksearch_hide();
}
};
this.ksearch_click=function(node){
if(this.ksearch_input){
this.ksearch_input.focus();
}
this.insert_recipient(node._rcm_id);
this.ksearch_hide();
};
this.ksearch_blur=function(){
if(this.ksearch_timer){
clearTimeout(this.ksearch_timer);
}
this.ksearch_value="";
this.ksearch_input=null;
this.ksearch_hide();
};
this.ksearch_hide=function(){
this.ksearch_selected=null;
if(this.ksearch_pane){
this.ksearch_pane.hide();
}
};
this.contactlist_keypress=function(list){
if(list.key_pressed==list.DELETE_KEY){
this.command("delete");
}
};
this.contactlist_select=function(list){
if(this.preview_timer){
clearTimeout(this.preview_timer);
}
var id,_136,_1=this;
if(id=list.get_single_selection()){
this.preview_timer=window.setTimeout(function(){
_1.load_contact(id,"show");
},200);
}else{
if(this.env.contentframe){
this.show_contentframe(false);
}
}
this.enable_command("compose",list.selection.length>0);
this.enable_command("edit",(id&&this.env.address_sources&&!this.env.address_sources[this.env.source].readonly)?true:false);
this.enable_command("delete",list.selection.length&&this.env.address_sources&&!this.env.address_sources[this.env.source].readonly);
return false;
};
this.list_contacts=function(src,page){
var _139="";
var _13a=window;
if(!src){
src=this.env.source;
}
if(page&&this.current_page==page&&src==this.env.source){
return false;
}
if(src!=this.env.source){
page=1;
this.env.current_page=page;
this.reset_qsearch();
}
this.select_folder(src,this.env.source);
this.env.source=src;
if(this.gui_objects.contactslist){
this.list_contacts_remote(src,page);
return;
}
if(this.env.contentframe&&window.frames&&window.frames[this.env.contentframe]){
_13a=window.frames[this.env.contentframe];
_139="&_framed=1";
}
if(this.env.search_request){
_139+="&_search="+this.env.search_request;
}
this.set_busy(true,"loading");
_13a.location.href=this.env.comm_path+(src?"&_source="+urlencode(src):"")+(page?"&_page="+page:"")+_139;
};
this.list_contacts_remote=function(src,page){
this.contact_list.clear(true);
this.show_contentframe(false);
this.enable_command("delete","compose",false);
var url=(src?"_source="+urlencode(src):"")+(page?(src?"&":"")+"_page="+page:"");
this.env.source=src;
if(this.env.search_request){
url+="&_search="+this.env.search_request;
}
this.set_busy(true,"loading");
this.http_request("list",url,true);
};
this.load_contact=function(cid,_13f,_140){
var _141="";
var _142=window;
if(this.env.contentframe&&window.frames&&window.frames[this.env.contentframe]){
_141="&_framed=1";
_142=window.frames[this.env.contentframe];
this.show_contentframe(true);
}else{
if(_140){
return false;
}
}
if(_13f&&(cid||_13f=="add")&&!this.drag_active){
this.set_busy(true);
_142.location.href=this.env.comm_path+"&_action="+_13f+"&_source="+urlencode(this.env.source)+"&_cid="+urlencode(cid)+_141;
}
return true;
};
this.copy_contact=function(cid,to){
if(!cid){
cid=this.contact_list.get_selection().join(",");
}
if(to!=this.env.source&&cid&&this.env.address_sources[to]&&!this.env.address_sources[to].readonly){
this.http_post("copy","_cid="+urlencode(cid)+"&_source="+urlencode(this.env.source)+"&_to="+urlencode(to));
}
};
this.delete_contacts=function(){
var _145=this.contact_list.get_selection();
if(!(_145.length||this.env.cid)||!confirm(this.get_label("deletecontactconfirm"))){
return;
}
var _146=new Array();
var qs="";
if(this.env.cid){
_146[_146.length]=this.env.cid;
}else{
var id;
for(var n=0;n<_145.length;n++){
id=_145[n];
_146[_146.length]=id;
this.contact_list.remove_row(id,(n==_145.length-1));
}
if(_145.length==1){
this.show_contentframe(false);
}
}
if(this.env.search_request){
qs+="&_search="+this.env.search_request;
}
this.http_post("delete","_cid="+urlencode(_146.join(","))+"&_source="+urlencode(this.env.source)+"&_from="+(this.env.action?this.env.action:"")+qs);
return true;
};
this.update_contact_row=function(cid,_14b,_14c){
var row;
if(this.contact_list.rows[cid]&&(row=this.contact_list.rows[cid].obj)){
for(var c=0;c<_14b.length;c++){
if(row.cells[c]){
$(row.cells[c]).html(_14b[c]);
}
}
if(_14c){
row.id="rcmrow"+_14c;
this.contact_list.remove_row(cid);
this.contact_list.init_row(row);
this.contact_list.selection[0]=_14c;
row.style.display="";
}
return true;
}
return false;
};
this.add_contact_row=function(cid,cols,_151){
if(!this.gui_objects.contactslist||!this.gui_objects.contactslist.tBodies[0]){
return false;
}
var _152=this.gui_objects.contactslist.tBodies[0];
var _153=_152.rows.length;
var even=_153%2;
var row=document.createElement("tr");
row.id="rcmrow"+cid;
row.className="contact "+(even?"even":"odd");
if(this.contact_list.in_selection(cid)){
row.className+=" selected";
}
for(var c in cols){
col=document.createElement("td");
col.className=String(c).toLowerCase();
col.innerHTML=cols[c];
row.appendChild(col);
}
this.contact_list.insert_row(row);
this.enable_command("export",(this.contact_list.rowcount>0));
};
this.init_subscription_list=function(){
var p=this;
this.subscription_list=new rcube_list_widget(this.gui_objects.subscriptionlist,{multiselect:false,draggable:true,keyboard:false,toggleselect:true});
this.subscription_list.addEventListener("select",function(o){
p.subscription_select(o);
});
this.subscription_list.addEventListener("dragstart",function(o){
p.drag_active=true;
});
this.subscription_list.addEventListener("dragend",function(o){
p.subscription_move_folder(o);
});
this.subscription_list.row_init=function(row){
var _15c=row.obj.getElementsByTagName("a");
if(_15c[0]){
_15c[0].onclick=function(){
p.rename_folder(row.id);
return false;
};
}
if(_15c[1]){
_15c[1].onclick=function(){
p.delete_folder(row.id);
return false;
};
}
row.obj.onmouseover=function(){
p.focus_subscription(row.id);
};
row.obj.onmouseout=function(){
p.unfocus_subscription(row.id);
};
};
this.subscription_list.init();
};
this.section_select=function(list){
var id=list.get_single_selection();
if(id){
var _15f="";
var _160=window;
this.set_busy(true);
if(this.env.contentframe&&window.frames&&window.frames[this.env.contentframe]){
_15f="&_framed=1";
_160=window.frames[this.env.contentframe];
}
_160.location.href=this.env.comm_path+"&_action=edit-prefs&_section="+id+_15f;
}
return true;
};
this.identity_select=function(list){
var id;
if(id=list.get_single_selection()){
this.load_identity(id,"edit-identity");
}
};
this.load_identity=function(id,_164){
if(_164=="edit-identity"&&(!id||id==this.env.iid)){
return false;
}
var _165="";
var _166=window;
if(this.env.contentframe&&window.frames&&window.frames[this.env.contentframe]){
_165="&_framed=1";
_166=window.frames[this.env.contentframe];
document.getElementById(this.env.contentframe).style.visibility="inherit";
}
if(_164&&(id||_164=="add-identity")){
this.set_busy(true);
_166.location.href=this.env.comm_path+"&_action="+_164+"&_iid="+id+_165;
}
return true;
};
this.delete_identity=function(id){
var _168=this.identity_list.get_selection();
if(!(_168.length||this.env.iid)){
return;
}
if(!id){
id=this.env.iid?this.env.iid:_168[0];
}
this.goto_url("delete-identity","_iid="+id+"&_token="+this.env.request_token,true);
return true;
};
this.focus_subscription=function(id){
var row,_16b;
var reg=RegExp("["+RegExp.escape(this.env.delimiter)+"]?[^"+RegExp.escape(this.env.delimiter)+"]+$");
if(this.drag_active&&this.env.folder&&(row=document.getElementById(id))){
if(this.env.subscriptionrows[id]&&(_16b=this.env.subscriptionrows[id][0])){
if(this.check_droptarget(_16b)&&!this.env.subscriptionrows[this.get_folder_row_id(this.env.folder)][2]&&(_16b!=this.env.folder.replace(reg,""))&&(!_16b.match(new RegExp("^"+RegExp.escape(this.env.folder+this.env.delimiter))))){
this.set_env("dstfolder",_16b);
$(row).addClass("droptarget");
}
}else{
if(this.env.folder.match(new RegExp(RegExp.escape(this.env.delimiter)))){
this.set_env("dstfolder",this.env.delimiter);
$(this.subscription_list.frame).addClass("droptarget");
}
}
}
};
this.unfocus_subscription=function(id){
var row=$("#"+id);
this.set_env("dstfolder",null);
if(this.env.subscriptionrows[id]&&row[0]){
row.removeClass("droptarget");
}else{
$(this.subscription_list.frame).removeClass("droptarget");
}
};
this.subscription_select=function(list){
var id,_171;
if((id=list.get_single_selection())&&this.env.subscriptionrows["rcmrow"+id]&&(_171=this.env.subscriptionrows["rcmrow"+id][0])){
this.set_env("folder",_171);
}else{
this.set_env("folder",null);
}
if(this.gui_objects.createfolderhint){
$(this.gui_objects.createfolderhint).html(this.env.folder?this.get_label("addsubfolderhint"):"");
}
};
this.subscription_move_folder=function(list){
var reg=RegExp("["+RegExp.escape(this.env.delimiter)+"]?[^"+RegExp.escape(this.env.delimiter)+"]+$");
if(this.env.folder&&this.env.dstfolder&&(this.env.dstfolder!=this.env.folder)&&(this.env.dstfolder!=this.env.folder.replace(reg,""))){
var reg=new RegExp("[^"+RegExp.escape(this.env.delimiter)+"]*["+RegExp.escape(this.env.delimiter)+"]","g");
var _174=this.env.folder.replace(reg,"");
var _175=this.env.dstfolder==this.env.delimiter?_174:this.env.dstfolder+this.env.delimiter+_174;
this.set_busy(true,"foldermoving");
this.http_post("rename-folder","_folder_oldname="+urlencode(this.env.folder)+"&_folder_newname="+urlencode(_175),true);
}
this.drag_active=false;
this.unfocus_subscription(this.get_folder_row_id(this.env.dstfolder));
};
this.create_folder=function(name){
if(this.edit_folder){
this.reset_folder_rename();
}
var form;
if((form=this.gui_objects.editform)&&form.elements["_folder_name"]){
name=form.elements["_folder_name"].value;
if(name.indexOf(this.env.delimiter)>=0){
alert(this.get_label("forbiddencharacter")+" ("+this.env.delimiter+")");
return false;
}
if(this.env.folder&&name!=""){
name=this.env.folder+this.env.delimiter+name;
}
this.set_busy(true,"foldercreating");
this.http_post("create-folder","_name="+urlencode(name),true);
}else{
if(form.elements["_folder_name"]){
form.elements["_folder_name"].focus();
}
}
};
this.rename_folder=function(id){
var temp,row,form;
if(temp=this.edit_folder){
this.reset_folder_rename();
if(temp==id){
return;
}
}
if(id&&this.env.subscriptionrows[id]&&(row=document.getElementById(id))){
var reg=new RegExp(".*["+RegExp.escape(this.env.delimiter)+"]");
this.name_input=document.createElement("input");
this.name_input.type="text";
this.name_input.value=this.env.subscriptionrows[id][0].replace(reg,"");
reg=new RegExp("["+RegExp.escape(this.env.delimiter)+"]?[^"+RegExp.escape(this.env.delimiter)+"]+$");
this.name_input.__parent=this.env.subscriptionrows[id][0].replace(reg,"");
this.name_input.onkeypress=function(e){
rcmail.name_input_keypress(e);
};
row.cells[0].replaceChild(this.name_input,row.cells[0].firstChild);
this.edit_folder=id;
this.name_input.select();
if(form=this.gui_objects.editform){
form.onsubmit=function(){
return false;
};
}
}
};
this.reset_folder_rename=function(){
var cell=this.name_input?this.name_input.parentNode:null;
if(cell&&this.edit_folder&&this.env.subscriptionrows[this.edit_folder]){
$(cell).html(this.env.subscriptionrows[this.edit_folder][1]);
}
this.edit_folder=null;
};
this.name_input_keypress=function(e){
var key=rcube_event.get_keycode(e);
if(key==13){
var _181=this.name_input?this.name_input.value:null;
if(this.edit_folder&&_181){
if(_181.indexOf(this.env.delimiter)>=0){
alert(this.get_label("forbiddencharacter")+" ("+this.env.delimiter+")");
return false;
}
if(this.name_input.__parent){
_181=this.name_input.__parent+this.env.delimiter+_181;
}
this.set_busy(true,"folderrenaming");
this.http_post("rename-folder","_folder_oldname="+urlencode(this.env.subscriptionrows[this.edit_folder][0])+"&_folder_newname="+urlencode(_181),true);
}
}else{
if(key==27){
this.reset_folder_rename();
}
}
};
this.delete_folder=function(id){
var _183=this.env.subscriptionrows[id][0];
if(this.edit_folder){
this.reset_folder_rename();
}
if(_183&&confirm(this.get_label("deletefolderconfirm"))){
this.set_busy(true,"folderdeleting");
this.http_post("delete-folder","_mboxes="+urlencode(_183),true);
this.set_env("folder",null);
$(this.gui_objects.createfolderhint).html("");
}
};
this.add_folder_row=function(name,_185,_186,_187){
if(!this.gui_objects.subscriptionlist){
return false;
}
for(var _188 in this.env.subscriptionrows){
if(this.env.subscriptionrows[_188]!=null&&!this.env.subscriptionrows[_188][2]){
break;
}
}
var _189,form;
var _18b=this.gui_objects.subscriptionlist.tBodies[0];
var id="rcmrow"+(_18b.childNodes.length+1);
var _18d=this.subscription_list.get_single_selection();
if(_186&&_186.id){
id=_186.id;
_188=_186.id;
}
if(!id||!(_189=document.getElementById(_188))){
this.goto_url("folders");
}else{
var row=this.clone_table_row(_189);
row.id=id;
if(_187&&(_187=this.get_folder_row_id(_187))){
_18b.insertBefore(row,document.getElementById(_187));
}else{
_18b.appendChild(row);
}
if(_186){
_18b.removeChild(_186);
}
}
this.env.subscriptionrows[row.id]=[name,_185,0];
row.cells[0].innerHTML=_185;
if(!_186){
row.cells[1].innerHTML="*";
}
if(!_186&&row.cells[2]&&row.cells[2].firstChild.tagName.toLowerCase()=="input"){
row.cells[2].firstChild.value=name;
row.cells[2].firstChild.checked=true;
}
if(!_186&&(form=this.gui_objects.editform)){
if(form.elements["_folder_oldname"]){
form.elements["_folder_oldname"].options[form.elements["_folder_oldname"].options.length]=new Option(name,name);
}
if(form.elements["_folder_name"]){
form.elements["_folder_name"].value="";
}
}
this.init_subscription_list();
if(_18d&&document.getElementById("rcmrow"+_18d)){
this.subscription_list.select_row(_18d);
}
if(document.getElementById(id).scrollIntoView){
document.getElementById(id).scrollIntoView();
}
};
this.replace_folder_row=function(_18f,_190,_191,_192){
var id=this.get_folder_row_id(_18f);
var row=document.getElementById(id);
this.add_folder_row(_190,_191,row,_192);
var form,elm;
if((form=this.gui_objects.editform)&&(elm=form.elements["_folder_oldname"])){
for(var i=0;i<elm.options.length;i++){
if(elm.options[i].value==_18f){
elm.options[i].text=_191;
elm.options[i].value=_190;
break;
}
}
form.elements["_folder_newname"].value="";
}
};
this.remove_folder_row=function(_198){
var row;
var id=this.get_folder_row_id(_198);
if(id&&(row=document.getElementById(id))){
row.style.display="none";
}
var form;
if((form=this.gui_objects.editform)&&form.elements["_folder_oldname"]){
for(var i=0;i<form.elements["_folder_oldname"].options.length;i++){
if(form.elements["_folder_oldname"].options[i].value==_198){
form.elements["_folder_oldname"].options[i]=null;
break;
}
}
}
if(form&&form.elements["_folder_newname"]){
form.elements["_folder_newname"].value="";
}
};
this.subscribe_folder=function(_19d){
if(_19d){
this.http_post("subscribe","_mbox="+urlencode(_19d));
}
};
this.unsubscribe_folder=function(_19e){
if(_19e){
this.http_post("unsubscribe","_mbox="+urlencode(_19e));
}
};
this.get_folder_row_id=function(_19f){
for(var id in this.env.subscriptionrows){
if(this.env.subscriptionrows[id]&&this.env.subscriptionrows[id][0]==_19f){
break;
}
}
return id;
};
this.clone_table_row=function(row){
var cell,td;
var _1a4=document.createElement("tr");
for(var n=0;n<row.cells.length;n++){
cell=row.cells[n];
td=document.createElement("td");
if(cell.className){
td.className=cell.className;
}
if(cell.align){
td.setAttribute("align",cell.align);
}
td.innerHTML=cell.innerHTML;
_1a4.appendChild(td);
}
return _1a4;
};
this.set_page_buttons=function(){
this.enable_command("nextpage",(this.env.pagecount>this.env.current_page));
this.enable_command("lastpage",(this.env.pagecount>this.env.current_page));
this.enable_command("previouspage",(this.env.current_page>1));
this.enable_command("firstpage",(this.env.current_page>1));
};
this.init_buttons=function(){
for(var cmd in this.buttons){
if(typeof cmd!="string"){
continue;
}
for(var i=0;i<this.buttons[cmd].length;i++){
var prop=this.buttons[cmd][i];
var elm=document.getElementById(prop.id);
if(!elm){
continue;
}
var _1aa=false;
if(prop.type=="image"){
elm=elm.parentNode;
_1aa=true;
}
elm._command=cmd;
elm._id=prop.id;
if(prop.sel){
elm.onmousedown=function(e){
return rcmail.button_sel(this._command,this._id);
};
elm.onmouseup=function(e){
return rcmail.button_out(this._command,this._id);
};
if(_1aa){
new Image().src=prop.sel;
}
}
if(prop.over){
elm.onmouseover=function(e){
return rcmail.button_over(this._command,this._id);
};
elm.onmouseout=function(e){
return rcmail.button_out(this._command,this._id);
};
if(_1aa){
new Image().src=prop.over;
}
}
}
}
};
this.set_button=function(_1af,_1b0){
var _1b1=this.buttons[_1af];
var _1b2,obj;
if(!_1b1||!_1b1.length){
return false;
}
for(var n=0;n<_1b1.length;n++){
_1b2=_1b1[n];
obj=document.getElementById(_1b2.id);
if(obj&&_1b2.type=="image"&&!_1b2.status){
_1b2.pas=obj._original_src?obj._original_src:obj.src;
if(obj.runtimeStyle&&obj.runtimeStyle.filter&&obj.runtimeStyle.filter.match(/src=['"]([^'"]+)['"]/)){
_1b2.pas=RegExp.$1;
}
}else{
if(obj&&!_1b2.status){
_1b2.pas=String(obj.className);
}
}
if(obj&&_1b2.type=="image"&&_1b2[_1b0]){
_1b2.status=_1b0;
obj.src=_1b2[_1b0];
}else{
if(obj&&typeof (_1b2[_1b0])!="undefined"){
_1b2.status=_1b0;
obj.className=_1b2[_1b0];
}
}
if(obj&&_1b2.type=="input"){
_1b2.status=_1b0;
obj.disabled=!_1b0;
}
}
};
this.set_alttext=function(_1b5,_1b6){
if(!this.buttons[_1b5]||!this.buttons[_1b5].length){
return;
}
var _1b7,obj,link;
for(var n=0;n<this.buttons[_1b5].length;n++){
_1b7=this.buttons[_1b5][n];
obj=document.getElementById(_1b7.id);
if(_1b7.type=="image"&&obj){
obj.setAttribute("alt",this.get_label(_1b6));
if((link=obj.parentNode)&&link.tagName.toLowerCase()=="a"){
link.setAttribute("title",this.get_label(_1b6));
}
}else{
if(obj){
obj.setAttribute("title",this.get_label(_1b6));
}
}
}
};
this.button_over=function(_1bb,id){
var _1bd=this.buttons[_1bb];
var _1be,elm;
if(!_1bd||!_1bd.length){
return false;
}
for(var n=0;n<_1bd.length;n++){
_1be=_1bd[n];
if(_1be.id==id&&_1be.status=="act"){
elm=document.getElementById(_1be.id);
if(elm&&_1be.over){
if(_1be.type=="image"){
elm.src=_1be.over;
}else{
elm.className=_1be.over;
}
}
}
}
};
this.button_sel=function(_1c1,id){
var _1c3=this.buttons[_1c1];
var _1c4,elm;
if(!_1c3||!_1c3.length){
return;
}
for(var n=0;n<_1c3.length;n++){
_1c4=_1c3[n];
if(_1c4.id==id&&_1c4.status=="act"){
elm=document.getElementById(_1c4.id);
if(elm&&_1c4.sel){
if(_1c4.type=="image"){
elm.src=_1c4.sel;
}else{
elm.className=_1c4.sel;
}
}
this.buttons_sel[id]=_1c1;
}
}
};
this.button_out=function(_1c7,id){
var _1c9=this.buttons[_1c7];
var _1ca,elm;
if(!_1c9||!_1c9.length){
return;
}
for(var n=0;n<_1c9.length;n++){
_1ca=_1c9[n];
if(_1ca.id==id&&_1ca.status=="act"){
elm=document.getElementById(_1ca.id);
if(elm&&_1ca.act){
if(_1ca.type=="image"){
elm.src=_1ca.act;
}else{
elm.className=_1ca.act;
}
}
}
}
};
this.set_pagetitle=function(_1cd){
if(_1cd&&document.title){
document.title=_1cd;
}
};
this.display_message=function(msg,type,hold){
if(!this.loaded){
this.pending_message=new Array(msg,type);
return true;
}
if(this.env.framed&&parent.rcmail){
return parent.rcmail.display_message(msg,type,hold);
}
if(!this.gui_objects.message){
return false;
}
if(this.message_timer){
clearTimeout(this.message_timer);
}
var cont=msg;
if(type){
cont="<div class=\""+type+"\">"+cont+"</div>";
}
var obj=$(this.gui_objects.message).html(cont).show();
if(type!="loading"){
obj.bind("mousedown",function(){
_1.hide_message();
return true;
});
}
if(!hold){
this.message_timer=window.setTimeout(function(){
_1.hide_message(true);
},this.message_time);
}
};
this.hide_message=function(fade){
if(this.gui_objects.message){
$(this.gui_objects.message).unbind()[(fade?"fadeOut":"hide")]();
}
};
this.select_folder=function(name,old){
if(this.gui_objects.folderlist){
var _1d6,_1d7;
if((_1d6=this.get_folder_li(old))){
$(_1d6).removeClass("selected").removeClass("unfocused");
}
if((_1d7=this.get_folder_li(name))){
$(_1d7).removeClass("unfocused").addClass("selected");
}
this.triggerEvent("selectfolder",{folder:name,old:old});
}
};
this.get_folder_li=function(name){
if(this.gui_objects.folderlist){
name=String(name).replace(this.identifier_expr,"_");
return document.getElementById("rcmli"+name);
}
return null;
};
this.set_message_coltypes=function(_1d9){
this.coltypes=_1d9;
var cell,col;
var _1dc=this.gui_objects.messagelist?this.gui_objects.messagelist.tHead:null;
for(var n=0;_1dc&&n<this.coltypes.length;n++){
col=this.coltypes[n];
if((cell=_1dc.rows[0].cells[n+1])&&(col=="from"||col=="to")){
if(cell.firstChild&&cell.firstChild.tagName.toLowerCase()=="a"){
cell.firstChild.innerHTML=this.get_label(this.coltypes[n]);
cell.firstChild.onclick=function(){
return rcmail.command("sort",this.__col,this);
};
cell.firstChild.__col=col;
}else{
cell.innerHTML=this.get_label(this.coltypes[n]);
}
cell.id="rcm"+col;
}else{
if(col=="subject"&&this.message_list){
this.message_list.subject_col=n+1;
}
}
}
};
this.add_message_row=function(uid,cols,_1e0,_1e1,_1e2){
if(!this.gui_objects.messagelist||!this.message_list){
return false;
}
if(this.message_list.background){
var _1e3=this.message_list.background;
}else{
var _1e3=this.gui_objects.messagelist.tBodies[0];
}
var _1e4=_1e3.rows.length;
var even=_1e4%2;
this.env.messages[uid]={deleted:_1e0.deleted?1:0,replied:_1e0.replied?1:0,unread:_1e0.unread?1:0,forwarded:_1e0.forwarded?1:0,flagged:_1e0.flagged?1:0};
var _1e6="message"+(even?" even":" odd")+(_1e0.unread?" unread":"")+(_1e0.deleted?" deleted":"")+(_1e0.flagged?" flagged":"")+(this.message_list.in_selection(uid)?" selected":"");
var row=document.createElement("tr");
row.id="rcmrow"+uid;
row.className=_1e6;
var icon=this.env.messageicon;
if(_1e0.deleted&&this.env.deletedicon){
icon=this.env.deletedicon;
}else{
if(_1e0.replied&&this.env.repliedicon){
if(_1e0.forwarded&&this.env.forwardedrepliedicon){
icon=this.env.forwardedrepliedicon;
}else{
icon=this.env.repliedicon;
}
}else{
if(_1e0.forwarded&&this.env.forwardedicon){
icon=this.env.forwardedicon;
}else{
if(_1e0.unread&&this.env.unreadicon){
icon=this.env.unreadicon;
}
}
}
}
var col=document.createElement("td");
col.className="icon";
col.innerHTML=icon?"<img src=\""+icon+"\" alt=\"\" />":"";
row.appendChild(col);
for(var n=0;n<this.coltypes.length;n++){
var c=this.coltypes[n];
col=document.createElement("td");
col.className=String(c).toLowerCase();
if(c=="flag"){
if(_1e0.flagged&&this.env.flaggedicon){
col.innerHTML="<img src=\""+this.env.flaggedicon+"\" alt=\"\" />";
}else{
if(!_1e0.flagged&&this.env.unflaggedicon){
col.innerHTML="<img src=\""+this.env.unflaggedicon+"\" alt=\"\" />";
}
}
}else{
if(c=="attachment"){
col.innerHTML=(_1e1&&this.env.attachmenticon?"<img src=\""+this.env.attachmenticon+"\" alt=\"\" />":"&nbsp;");
}else{
col.innerHTML=cols[c];
}
}
row.appendChild(col);
}
this.message_list.insert_row(row,_1e2);
if(_1e2&&this.env.pagesize&&this.message_list.rowcount>this.env.pagesize){
var uid=this.message_list.get_last_row();
this.message_list.remove_row(uid);
this.message_list.clear_selection(uid);
}
};
this.offline_message_list=function(flag){
if(this.message_list){
this.message_list.set_background_mode(flag);
}
};
this.set_rowcount=function(text){
$(this.gui_objects.countdisplay).html(text);
this.set_page_buttons();
};
this.set_mailboxname=function(_1ee){
if(this.gui_objects.mailboxname&&_1ee){
this.gui_objects.mailboxname.innerHTML=_1ee;
}
};
this.set_quota=function(_1ef){
if(_1ef&&this.gui_objects.quotadisplay){
$(this.gui_objects.quotadisplay).html(_1ef);
}
};
this.set_unread_count=function(mbox,_1f1,_1f2){
if(!this.gui_objects.mailboxlist){
return false;
}
this.env.unread_counts[mbox]=_1f1;
this.set_unread_count_display(mbox,_1f2);
};
this.set_unread_count_display=function(mbox,_1f4){
var reg,_1f6,item,_1f8,_1f9,div;
if(item=this.get_folder_li(mbox)){
_1f8=this.env.unread_counts[mbox]?this.env.unread_counts[mbox]:0;
_1f6=item.getElementsByTagName("a")[0];
reg=/\s+\([0-9]+\)$/i;
_1f9=0;
if((div=item.getElementsByTagName("div")[0])&&div.className.match(/collapsed/)){
for(var k in this.env.unread_counts){
if(k.indexOf(mbox+this.env.delimiter)==0){
_1f9+=this.env.unread_counts[k];
}
}
}
if(_1f8&&_1f6.innerHTML.match(reg)){
_1f6.innerHTML=_1f6.innerHTML.replace(reg," ("+_1f8+")");
}else{
if(_1f8){
_1f6.innerHTML+=" ("+_1f8+")";
}else{
_1f6.innerHTML=_1f6.innerHTML.replace(reg,"");
}
}
reg=new RegExp(RegExp.escape(this.env.delimiter)+"[^"+RegExp.escape(this.env.delimiter)+"]+$");
if(mbox.match(reg)){
this.set_unread_count_display(mbox.replace(reg,""),false);
}
if((_1f8+_1f9)>0){
$(item).addClass("unread");
}else{
$(item).removeClass("unread");
}
}
reg=/^\([0-9]+\)\s+/i;
if(_1f4&&document.title){
var _1fc=String(document.title);
var _1fd="";
if(_1f8&&_1fc.match(reg)){
_1fd=_1fc.replace(reg,"("+_1f8+") ");
}else{
if(_1f8){
_1fd="("+_1f8+") "+_1fc;
}else{
_1fd=_1fc.replace(reg,"");
}
}
this.set_pagetitle(_1fd);
}
};
this.new_message_focus=function(){
if(this.env.framed&&window.parent){
window.parent.focus();
}else{
window.focus();
}
};
this.toggle_prefer_html=function(_1fe){
var _1ff;
if(_1ff=document.getElementById("rcmfd_addrbook_show_images")){
_1ff.disabled=!_1fe.checked;
}
};
this.set_headers=function(_200){
if(this.gui_objects.all_headers_row&&this.gui_objects.all_headers_box&&_200){
$(this.gui_objects.all_headers_box).html(_200).show();
if(this.env.framed&&parent.rcmail){
parent.rcmail.set_busy(false);
}else{
this.set_busy(false);
}
}
};
this.load_headers=function(elem){
if(!this.gui_objects.all_headers_row||!this.gui_objects.all_headers_box||!this.env.uid){
return;
}
$(elem).removeClass("show-headers").addClass("hide-headers");
$(this.gui_objects.all_headers_row).show();
elem.onclick=function(){
rcmail.hide_headers(elem);
};
if(!this.gui_objects.all_headers_box.innerHTML){
this.display_message(this.get_label("loading"),"loading",true);
this.http_post("headers","_uid="+this.env.uid);
}
};
this.hide_headers=function(elem){
if(!this.gui_objects.all_headers_row||!this.gui_objects.all_headers_box){
return;
}
$(elem).removeClass("hide-headers").addClass("show-headers");
$(this.gui_objects.all_headers_row).hide();
elem.onclick=function(){
rcmail.load_headers(elem);
};
};
this.html2plain=function(_203,id){
var url=this.env.bin_path+"html2text.php";
var _206=this;
this.set_busy(true,"converting");
console.log("HTTP POST: "+url);
$.ajax({type:"POST",url:url,data:_203,contentType:"application/octet-stream",error:function(o){
_206.http_error(o);
},success:function(data){
_206.set_busy(false);
$(document.getElementById(id)).val(data);
console.log(data);
}});
};
this.plain2html=function(_209,id){
this.set_busy(true,"converting");
$(document.getElementById(id)).val("<pre>"+_209+"</pre>");
this.set_busy(false);
};
this.redirect=function(url,lock){
if(lock||lock===null){
this.set_busy(true);
}
if(this.env.framed&&window.parent){
parent.location.href=url;
}else{
location.href=url;
}
};
this.goto_url=function(_20d,_20e,lock){
var _210=_20e?"&"+_20e:"";
this.redirect(this.env.comm_path+"&_action="+_20d+_210,lock);
};
this.http_request=function(_211,_212,lock){
_212+=(_212?"&":"")+"_remote=1";
var url=this.env.comm_path+"&_action="+_211+"&"+_212;
console.log("HTTP POST: "+url);
jQuery.get(url,{_unlock:(lock?1:0)},function(data){
_1.http_response(data);
},"json");
};
this.http_post=function(_216,_217,lock){
var url=this.env.comm_path+"&_action="+_216;
if(_217&&typeof (_217)=="object"){
_217._remote=1;
_217._unlock=(lock?1:0);
}else{
_217+=(_217?"&":"")+"_remote=1"+(lock?"&_unlock=1":"");
}
console.log("HTTP POST: "+url);
jQuery.post(url,_217,function(data){
_1.http_response(data);
},"json");
};
this.http_response=function(_21b){
var _21c="";
if(_21b.unlock){
this.set_busy(false);
}
if(_21b.env){
this.set_env(_21b.env);
}
if(typeof _21b.texts=="object"){
for(var name in _21b.texts){
if(typeof _21b.texts[name]=="string"){
this.add_label(name,_21b.texts[name]);
}
}
}
if(_21b.exec){
console.log(_21b.exec);
eval(_21b.exec);
}
if(_21b.callbacks&&_21b.callbacks.length){
for(var i=0;i<_21b.callbacks.length;i++){
this.triggerEvent(_21b.callbacks[i][0],_21b.callbacks[i][1]);
}
}
switch(_21b.action){
case "delete":
if(this.task=="addressbook"){
var uid=this.contact_list.get_selection();
this.enable_command("compose",(uid&&this.contact_list.rows[uid]));
this.enable_command("delete","edit",(uid&&this.contact_list.rows[uid]&&this.env.address_sources&&!this.env.address_sources[this.env.source].readonly));
this.enable_command("export",(this.contact_list&&this.contact_list.rowcount>0));
}
case "moveto":
if(this.env.action=="show"){
this.enable_command("reply","reply-all","forward","delete","mark","print","open","edit","viewsource","download",true);
}else{
if(this.message_list){
this.message_list.init();
}
}
break;
case "purge":
case "expunge":
if(!this.env.messagecount&&this.task=="mail"){
if(this.env.contentframe){
this.show_contentframe(false);
}
this.enable_command("show","reply","reply-all","forward","moveto","delete","mark","viewsource","open","edit","download","print","load-attachment","purge","expunge","select-all","select-none","sort",false);
}
break;
case "check-recent":
case "getunread":
case "list":
if(this.task=="mail"){
if(this.message_list&&_21b.action=="list"){
this.msglist_select(this.message_list);
}
this.enable_command("show","expunge","select-all","select-none","sort",(this.env.messagecount>0));
this.enable_command("purge",this.purge_mailbox_test());
if(_21b.action=="list"){
this.triggerEvent("listupdate",{folder:this.env.mailbox,rowcount:this.message_list.rowcount});
}
}else{
if(this.task=="addressbook"){
this.enable_command("export",(this.contact_list&&this.contact_list.rowcount>0));
if(_21b.action=="list"){
this.triggerEvent("listupdate",{folder:this.env.source,rowcount:this.contact_list.rowcount});
}
}
}
break;
}
};
this.http_error=function(_220,_221,err){
var _223=_220.statusText;
this.set_busy(false);
_220.abort();
if(_223){
this.display_message(this.get_label("servererror")+" ("+_223+")","error");
}
};
this.send_keep_alive=function(){
var d=new Date();
this.http_request("keep-alive","_t="+d.getTime());
};
this.check_for_recent=function(_225){
if(this.busy){
return;
}
if(_225){
this.set_busy(true,"checkingmail");
}
var _226="_t="+(new Date().getTime());
if(this.gui_objects.messagelist){
_226+="&_list=1";
}
if(this.gui_objects.quotadisplay){
_226+="&_quota=1";
}
if(this.env.search_request){
_226+="&_search="+this.env.search_request;
}
this.http_request("check-recent",_226,true);
};
this.get_single_uid=function(){
return this.env.uid?this.env.uid:(this.message_list?this.message_list.get_single_selection():null);
};
this.get_single_cid=function(){
return this.env.cid?this.env.cid:(this.contact_list?this.contact_list.get_single_selection():null);
};
this.get_caret_pos=function(obj){
if(typeof (obj.selectionEnd)!="undefined"){
return obj.selectionEnd;
}else{
if(document.selection&&document.selection.createRange){
var _228=document.selection.createRange();
if(_228.parentElement()!=obj){
return 0;
}
var gm=_228.duplicate();
if(obj.tagName=="TEXTAREA"){
gm.moveToElementText(obj);
}else{
gm.expand("textedit");
}
gm.setEndPoint("EndToStart",_228);
var p=gm.text.length;
return p<=obj.value.length?p:-1;
}else{
return obj.value.length;
}
}
};
this.set_caret_pos=function(obj,pos){
if(obj.setSelectionRange){
obj.setSelectionRange(pos,pos);
}else{
if(obj.createTextRange){
var _22d=obj.createTextRange();
_22d.collapse(true);
_22d.moveEnd("character",pos);
_22d.moveStart("character",pos);
_22d.select();
}
}
};
this.lock_form=function(form,lock){
if(!form||!form.elements){
return;
}
var type;
for(var n=0;n<form.elements.length;n++){
type=form.elements[n];
if(type=="hidden"){
continue;
}
form.elements[n].disabled=lock;
}
};
};
rcube_webmail.prototype.addEventListener=rcube_event_engine.prototype.addEventListener;
rcube_webmail.prototype.removeEventListener=rcube_event_engine.prototype.removeEventListener;
rcube_webmail.prototype.triggerEvent=rcube_event_engine.prototype.triggerEvent;

