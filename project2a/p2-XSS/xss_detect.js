function notifyUser() {
	/* chrome notification function...  */
  console.log("in notifyUser... ");
}

chrome.webRequest.onBeforeRequest.addListener(function (details) {
	 console.log(details.url); // use console.log wherever required...




	/* define your regular expression(s)... Keep the variables name as it is...*/

	var script_start_re = "/(<\s*?(script)\s*?>.*?<\/\s*?(script)\s*?>)/igs";  /* regular expression corresponding to starting script tag... */ //multiline case insensitive
	var script_end_re  /* regular expression corresponding to ending script tag... (if required)... */

	if(details.method == "POST") {
		console.log("taf.. POST");
    //console.log($('form').serialize());

		/* store POST form data.... */



	} else if(details.method == "GET") {
		console.log("traci... GET");
    //console.log($('form').serialize());
		/* store GET data ... */

	}

	/* Compare your stored value with the regular expression(s) for both, GET and POST method...  */

	;
},
{urls: ["<all_urls>"]}, ["blocking","requestBody"]);
