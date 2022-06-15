var currentPage = 1;
var isEndOfScroll = false;

window.onload = function() {
  window.addEventListener('scroll', function(event)
  {
      var element = window.document.scrollingElement;
      if (element.scrollHeight - element.scrollTop === element.clientHeight && !isEndOfScroll)
      {
          fetchData();
      }
  });
};

function fetchData() {
    var keyword = document.getElementById('result-keyword').value;
    var category = document.getElementById('result-category').value;
    var start = document.getElementById('result-start').value;
    var end = document.getElementById('result-end').value;
    var weekday = document.getElementById('result-weekday').value;

    currentPage ++;

    var httpRequest = new XMLHttpRequest();
    httpRequest.addEventListener("load", (e) => {
        var jsonResponse = JSON.parse(e.target.responseText);
        console.log(jsonResponse)
        jsonResponse.object_list.forEach(data => appendItem(data));
        if (jsonResponse.length < 8 || jsonResponse.has_next_page === false) isEndOfScroll = true;
    });
    httpRequest.open("GET", "/search/json/?page=" + currentPage
        + "&keyword=" + keyword + "&category=" + category + "&start=" + start + "&end=" + end + "&weekday=" + weekday);
    httpRequest.send();
}

function appendItem(data) {
    var template = document.getElementById("restaurant-template");
    var body = document.getElementById("search-result")
    var clone = template.content.cloneNode(true);
    clone.querySelector(".item-category").textContent = data.category_name;
    clone.querySelector(".item-name").textContent = data.name;
    clone.querySelector(".item-address").textContent = data.address;

    if (clone.querySelector(".item-link") != null) {
    	var link = clone.querySelector(".item-link").href;
	    link = link.replace("/0/", "/" + data.id + "/");
	    clone.querySelector(".item-link").href = link;
    }

    var finalUrl = data.image.replace("/media/https%3A", "https:/"); // 외부 url 대응
    clone.querySelector(".item-image").src = finalUrl;

    body.appendChild(clone);
}