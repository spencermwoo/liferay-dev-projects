
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

function getJSON(url){
	var json = JSON.parse(get(url));

	return json;
}

function getString(url){
	rr = get(url);
	// console.log(rr);
	return String(rr);
}



//THESE CAN BE DIFFERENT ACROSS VERSIONS.  Hack first -- fix with a map pair?
function extractAlloyEditor(json){
	return stripVersion(json['dependencies']['alloyeditor']);
}
function extractClay(json){
	return stripVersion(json['dependencies']['clay']);
}
function extractJQuery(json){
	return stripVersion(json['dependencies']['jquery']);
}

function extractSenna(json){
	return stripVersion(json['dependencies']['senna']);	
}

//UNIQUES
//THIS IS AN EXAMPLE^.  BETTER DESIGN LATER
function extractLexicon(str){
	str = str.match(/(lexiconVersion = ).+/g)[0];

	return stripVersion(str)
}

// Util
function stripVersion(str){
	// return str;
	return str.match(/[\d.]+/g)[0];
}


// Fetch
// Can use string builder...
function fetchLibrary(arr, func, str){
	ret_str = str || "";

	for(var i = 0 ; i < arr.length; i++){
		ret_str += "\n" + versions[i];

		try{
			json = getJSON(arr[i]);

			ret_str += " : " + func(json);
		} catch (err) {
			//try not json
			try{
				if(str === "Clay"){
					str = getString(arr[i]);

					ret_str += " : " + extractLexicon(str);
				} else {
					console.log(str);
					throw err;
				}
			} catch (err) {
				console.log("Failure at " + arr[i]);
			}
		}
	}

	return ret_str;
}

function fetchAlloyEditor(){
	return fetchLibrary(alloyeditor, extractAlloyEditor, "AlloyEditor");
}

function fetchClay(){
	return fetchLibrary(clay, extractClay, "Clay");
}
function fetchJQuery(){
	//jq same endpoint as clay
	return fetchLibrary(jquery, extractJQuery, "jQuery");
}

function fetchSenna(){
	return fetchLibrary(senna, extractSenna, "Senna");
}

function fetch(){
	// var value = "asdfsa";

	// console.log(fetchAlloyEditor());
	// console.log(fetchClay());
	// console.log(fetchSenna());
	console.log(fetchJQuery());

	// console.log(output);

	// getJSON(alloyeditor[0]);
	// console.log(value);
}