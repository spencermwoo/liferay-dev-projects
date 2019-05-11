
//versions length is always the same as each of these arrays -- perhaps I can make that explicit by design

var versions = ["master", "7.1.x", "7.0.x"];

var alloyeditor = ["https://raw.githubusercontent.com/liferay/liferay-portal/master/modules/apps/frontend-editor/frontend-editor-alloyeditor-web/package.json", 
					"https://raw.githubusercontent.com/liferay/liferay-portal/7.1.x/modules/apps/frontend-editor/frontend-editor-alloyeditor-web/package.json",
					"https://raw.githubusercontent.com/liferay/liferay-portal/7.0.x/modules/apps/foundation/frontend-editor/frontend-editor-alloyeditor-web/package.json"
					];

var senna = ["https://raw.githubusercontent.com/liferay/liferay-portal/master/modules/apps/frontend-js/frontend-js-spa-web/package.json", 
				"https://raw.githubusercontent.com/liferay/liferay-portal/7.1.x/modules/apps/frontend-js/frontend-js-spa-web/package.json",
				"https://raw.githubusercontent.com/liferay/liferay-portal/7.0.x/modules/apps/foundation/frontend-js/frontend-js-spa-web/package.json"];

var clay = ["https://raw.githubusercontent.com/liferay/liferay-portal/master/modules/apps/frontend-js/frontend-js-web/package.json",
				"https://raw.githubusercontent.com/liferay/liferay-portal/7.1.x/modules/apps/frontend-js/frontend-js-web/package.json",
				"https://raw.githubusercontent.com/liferay/liferay-portal/7.0.x/modules/apps/foundation/frontend-js/frontend-js-web/build.gradle"];

var jquery = clay;


// dynamic build above arrays later?
// var url = "https://raw.githubusercontent.com/liferay/liferay-portal/";
// var modules = "/modules/apps/";
// var foundation = "foundation/";


// var alloyeditor_path = "frontend-editor/frontend-editor-alloyeditor-web/package.json";
// var senna_path = "frontend-js/frontend-js-spa-web/package.json";





// var versions = ["https://raw.githubusercontent.com/liferay/liferay-portal/master/modules/apps/", "https://raw.githubusercontent.com/liferay/liferay-portal/7.1.x/modules/apps/"]


// let alloyeditor = Array(versions.length).fill().map((i) => url + versions[i] + modules + if(i==version.length-1){ foundation + } alloyeditor_path)
// var alloyeditor = [];
// var senna = [];



// could even just go to tree and /find file but -- hardcoding url should work for a while

function get(url){
    var Httpreq = new XMLHttpRequest(); // a new request
    
    Httpreq.open("GET", url, false);
    Httpreq.send(null);

    return Httpreq.responseText;          
}

function get_json(url){
	var json = JSON.parse(get(url));

	return json;
}

function get_string(url){
	return String(get(url));
}


function extract_version(str){
	return str.match(/[\d.]+/g)[0];
}

function extract_json(json, match){
	return extract_version(json['dependencies'][match]);
}

function extract_string(str, regex){
	str = str.match(regex)[0];

	return extract_version(str);
}

// Fetch
// Can use string builder...
function fetch_library(arr, str){
	ret_str = str || "";

	for(var i = 0 ; i < arr.length; i++){
		ret_str += "\n" + versions[i];

		try{
			json = get_json(arr[i]);

			// ret_str += " : " + func(json);
			ret_str += " : " + extract_json(json, str);
		} catch (err) {
			//try not json
			try{
				tmp_str = get_string(arr[i]);

				if(str === "clay"){
					regex = new RegExp("(lexiconVersion = ).+");
				} else if(str === "jquery"){
					regex = new RegExp("(jQueryVersion = ).+");
					// regex = new RegExp("(" + str + "Version = ).+");
				} else {
					throw err;
				}

				ret_str += " : " + extract_string(tmp_str, regex);
			} catch (err) {
				// console.log("Failure at " + arr[i]);
				ret_str += " : Unknown";
			}
		}
	}

	return ret_str;
}

function fetch_alloyeditor(){
	return fetch_library(alloyeditor, "alloyeditor");
}

function fetch_clay(){
	return fetch_library(clay, "clay");
}
function fetch_jquery(){
	return fetch_library(clay, "jquery"); // clay endpoint
}

function fetch_senna(){
	return fetch_library(senna, "senna");
}

function fetch(){
	console.log(fetch_alloyeditor());
	console.log(fetch_clay());
	console.log(fetch_jquery());
	console.log(fetch_senna());
}