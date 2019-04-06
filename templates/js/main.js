let host = "https://extra-snickdx.c9users.io:8080";


function ajaxPost(url, data, callback){
    let xhr = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        callback(this.responseText);
      }
    };
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(data);
}

function ajaxPut(url, data, callback){
    let xhr = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        callback(this.responseText);
      }
    };
    xhr.open("PUT", url);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(data);
}

function ajaxGet(url, callback){
    let xhr = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        callback(this.responseText);
      }
    };
    xhr.open("GET", url);
    xhr.send();
}

function ajaxDelete(url, callback){
    let xhr = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        callback(this.responseText);
      }
    };
    xhr.open("DELETE", url);
    xhr.send();
}

function deleteRecord(id){
    ajaxDelete(`${host}/api/persons/${id}`, loadRecords);
}

function clearForm(id){
    let form = document.querySelector(`#${{id}}`);
    form.elements.map(ele => ele.value="");
}

function updateRecord(){
    
    let form = document.querySelector("#updateForm");
	let record = {
		id: form.elements['id'].value,
		name: form.elements['name'].value,
		country: form.elements['country'].value
	};
	clearForm("updateForm");
    ajaxPut(`${host}/api/persons/${record.id}`, record, loadRecords);
}

function createRecord(){
    let form = document.querySelector("#createForm");
	let record = {
		id: form.elements['id'].value,
		name: form.elements['name'].value,
		country: form.elements['country'].value
	};
	clearForm("createForm");
    ajaxPost(`${host}/api/persons`, record, loadRecords);
}

function recordsHandler(records){
    let tableHtml = "";
    let selectHtml = "";
    
    for(rec of records){
         tableHTML+=`<tr>
                        <td>${{rec.id}}</td>
                        <td>${{rec.name}}</td>
                        <td>${{rec.country}}</td>
                        <td>${rec.date_created}}</td>
                        <td>
                            <input type="button" value="delete" onclic="deleteRecord(${{rec.id}})>DELETE</a>
                        </td>
                    </tr>`;
        selectHTML+=`<option>${{rec.id}}<option>`;
    }
    document.querySelector("#recSelect").innerHTML = selectHTML;
    document.querySelector("#list").innerHTML = tableHTML;
}

function loadRecords(){
    console.log("loading records");
    ajaxGet(`{{host}}/persons`, recordsHandler);
}

console.log("hello");

window.addEventListener('load', function() {
    console.log('All assets are loaded');
    loadRecords();

})



