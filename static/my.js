let total = 0;

function getData(loc) {
  boat = searchBoat(loc);
  if (boat["Away"] == "Y") {
    document.getElementById("bname").innerHTML = boat["Boat Name"] + " - AWAY";
  } else {
    document.getElementById("bname").innerHTML = boat["Boat Name"];
  }
  document.getElementById("blength").innerHTML = boat["Length"] + "m " + boat["Type"];
  document.getElementById("bloc").innerHTML = "Berth: " + boat["Loc"];
  document.getElementById("bowner").innerHTML = "Owner: " + boat["Owner"];
  document.getElementById("bremark").innerHTML = "Notes: " + boat["Remark"];
  document.getElementById("bphone").innerHTML = "Phone: " + boat["Phone"];
  document.getElementById("bpaid").innerHTML = "Paid: " + boat["Paid"];
}

function searchBoat(location) {
  for (let i = 0; i < boaty.length; i++) {
    if (boaty[i]["Loc"] == location) {
      return(boaty[i]);
    }
  }
}

function showBoat() {
  for (let i = 0; i < boaty.length; i++) {
    let berth = boaty[i]['Loc'];
    let berthNum = berth.slice(1);
    let boat_d = document.getElementById(berth);
    if (boat_d != null && boaty[i]["Away"] != 'Y') {
      console.log(berth);
      boat_d.classList.add("show");
      total = total + 1
    }
    if (boat_d != null && boaty[i]["Away"] == 'Y') {
      boat_d.classList.add("away");
    }
    if (berth[0] == 'C' && berthNum < 10) {
      boat_d.style.height = boaty[i]['Length']*3 + 'px';
    }
    if (berth[0] == 'A' && berthNum < 11) {
      boat_d.style.height = boaty[i]['Length']*3.5 + 'px';
    }
    if (berth[0] == 'B' && berthNum < 16) {
      boat_d.style.width = boaty[i]['Length']*4 + 'px';
    }
    if (berth[0] == 'B' && boaty[i]['Length'] > 17) {
      boat_d.style.left = '370px';
    }
    if (berth[0] == 'D' && berthNum < 4) {
      boat_d.style.height = boaty[i]['Length']*3 + 'px';
    }
    if (berth[0] == 'D' && berthNum > 3 && berthNum < 17) {
      boat_d.style.width = boaty[i]['Length']*3 + 'px';
    }
    if (berth[0] == 'D' && berthNum > 32) {
      boat_d.style.height = boaty[i]['Length']*3 + 'px';
    }
  }
}

function satellite() {
  var x = document.getElementsByTagName("H6");
  var i;
  for (i = 0; i < x.length; i++) {
    x[i].style.color = "white";
  }
  document.getElementById("colorbut").classList.add("hide");
  map = document.getElementById("map");
  map.classList.remove("cmap");
  map.classList.remove("dark");
  map.classList.add("gmap");
  land = document.getElementById("land");
  land.classList.add("hide");
  land2 = document.getElementById("land2");
  land2.classList.add("hide");
  land3 = document.getElementById("land3");
  land3.classList.add("hide");
}

function cartoon() {
  var x = document.getElementsByTagName("H6");
  var i;
  for (i = 0; i < x.length; i++) {
    x[i].style.color = "black";
  }
  document.getElementById("colorbut").classList.remove("hide");
  map = document.getElementById("map");
  map.classList.remove("gmap");
  map.classList.add("cmap");
  map.classList.add("dark");
  land = document.getElementById("land");
  land.classList.remove("hide");
  land2 = document.getElementById("land2");
  land2.classList.remove("hide");
  land3 = document.getElementById("land3");
  land3.classList.remove("hide");
}

function light() {
  map = document.getElementById("map");
  map.classList.remove("dark");
  map.classList.add("light");
  land = document.getElementById("land");
  land.classList.remove("landDark");
  land.classList.add("landLight");
  land2 = document.getElementById("land2");
  land2.classList.remove("landDark");
  land2.classList.add("landLight");
  land3 = document.getElementById("land3");
  land3.classList.remove("landDark");
  land3.classList.add("landLight");
}

function dark() {
  map = document.getElementById("map");
  map.classList.remove("light");
  map.classList.add("dark");
  land = document.getElementById("land");
  land.classList.remove("landLight");
  land.classList.add("landDark");
  land2 = document.getElementById("land2");
  land2.classList.remove("landLight");
  land2.classList.add("landDark");
  land3 = document.getElementById("land3");
  land3.classList.remove("landLight");
  land3.classList.add("landDark");
}

showBoat()
document.getElementById("date").innerHTML = total + " Boats";
