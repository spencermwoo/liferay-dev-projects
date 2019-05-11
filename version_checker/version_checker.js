
var alloyeditor = ["https://raw.githubusercontent.com/liferay/liferay-portal/master/modules/apps/frontend-editor/frontend-editor-alloyeditor-web/package.json", 
					"https://raw.githubusercontent.com/liferay/liferay-portal/7.1.x/modules/apps/frontend-editor/frontend-editor-alloyeditor-web/package.json",
					"https://raw.githubusercontent.com/liferay/liferay-portal/7.0.x/modules/apps/foundation/frontend-editor/frontend-editor-alloyeditor-web/package.json"
					];

var senna = ["https://raw.githubusercontent.com/liferay/liferay-portal/master/modules/apps/frontend-js/frontend-js-spa-web/package.json", 
				"https://raw.githubusercontent.com/liferay/liferay-portal/7.1.x./modules/apps/frontend-js/frontend-js-spa-web/package.json",
				"https://raw.githubusercontent.com/liferay/liferay-portal/7.0.x/modules/apps/foundation/frontend-js/frontend-js-spa-web/package.json"];

//clay, lexicon
var css = ["https://github.com/liferay/liferay-portal/blob/master/modules/apps/frontend-js/frontend-js-web/package.json",
"https://github.com/liferay/liferay-portal/blob/7.1.x/modules/apps/frontend-js/frontend-js-web/package.json",
"https://github.com/liferay/liferay-portal-ee/blob/7.0.x/modules/apps/foundation/frontend-js/frontend-js-web/build.gradle"];

var jquery = ["https://github.com/liferay/liferay-portal-ee/blob/7.0.x/modules/apps/foundation/frontend-js/frontend-js-web/build.gradle"];

var url = "https://raw.githubusercontent.com/liferay/liferay-portal/";
var versions = ["master", "7.1.x", "7.0.x"];
var modules = "/modules/apps/";
// var versions = ["https://raw.githubusercontent.com/liferay/liferay-portal/master/modules/apps/", "https://raw.githubusercontent.com/liferay/liferay-portal/7.1.x/modules/apps/"]

var foundation = "foundation/";

var alloyeditor_path = "frontend-editor/frontend-editor-alloyeditor-web/package.json";
var senna_path = "frontend-js/frontend-js-spa-web/package.json";

// could even just go to tree and /find file but -- hardcoding url should work for a while

function getJSON(url){
	json = $.get(url)
}
