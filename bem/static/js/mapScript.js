"use strict";

let map, mapEvent;

class Event {
  id = (Date.now() + "").slice(-10);

  constructor(coords, location, date, time) {
    this.coords = coords; //[lat, lng]
    this.location = location;
    this.date = date;
    this.time = time;
  }

  _setDescription() {
    const day = `${this.date[0].toUpperCase()}${this.date.slice(
      1,
      3
    )} ${this.date.slice(3)}`;
    this.description = `Event on ${day}`;
  }
}

class All extends Event {
  type = "all";
  constructor(coords, location, date, time) {
    super(coords, location, date, time);
    this._setDescription();
  }
}
class Knockout extends Event {
  type = "knockout";
  constructor(coords, location, date, time) {
    super(coords, location, date, time);
    this._setDescription();
  }
}

// const all1 = new All([39, -12], "Dec 2", "6:30pm");
/////////////////
///////APP ARCHITECTURE

const form = document.querySelector(".form");
const containerEvents = document.querySelector(".events");
const inputLocation = document.querySelector(".form__input--location");
const inputType = document.querySelector(".form__input--type");
const inputDate = document.querySelector(".form__input--date");
const inputTime = document.querySelector(".form__input--time");
const inputFee = document.querySelector(".form__input--fee");

class App {
  #map;
  #mapZoomLevel = 13;
  #mapEvent;
  #events = [];

  constructor() {
    this._getPosition();

    //get data from local storage
    this._getLocalStorage();

    form.addEventListener("submit", this._newWorkout.bind(this));
    containerEvents.addEventListener("click", this._moveToPopup.bind(this));
  }

  _getPosition() {
    if (navigator.geolocation)
      navigator.geolocation.getCurrentPosition(
        this._loadMap.bind(this),
        function () {
          alert("Could not get your position");
        },
        {
          enableHighAccuracy: true,
        }
      );
  }

  _loadMap(position) {
    //   12.9283947,77.6061809
    // const { latitude } = position.coords;
    // const { longitude } = position.coords;

    const latitude = 12.9283947;
    const longitude = 77.6061809;
    console.log(latitude, longitude);
    console.log(`https://www.google.com/maps/@${latitude},${longitude}`);
    const coords = [latitude, longitude];

    this.#map = L.map("map").setView(coords, this.#mapZoomLevel);

    L.tileLayer("http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}", {
      maxZoom: 20,
      subdomains: ["mt0", "mt1", "mt2", "mt3"],
    }).addTo(this.#map);

    //handling clicks on map

    this.#map.on("click", this._showForm.bind(this));

    this.#events.forEach((ev) => {
      this._renderEventMarker(ev);
    });
  }

  _showForm(mapE) {
    this.#mapEvent = mapE;
    form.classList.remove("hidden");
    inputLocation.focus();
  }

  _hideForm() {
    //Empty inputs
    inputLocation.value =
      inputDate.value =
      inputTime.value =
      inputFee.value =
        "";

    form.style.display = "none";
    form.classList.add("hidden");
    setTimeout(() => (form.style.display = "grid"), 1000);
  }

  _newWorkout(e) {
    e.preventDefault();
    //Get data from form
    const location = inputLocation.value;
    const type = inputType.value;
    const date = inputDate.value;
    const time = inputTime.value;
    const fee = +inputFee.value;
    const { lat, lng } = this.#mapEvent.latlng;
    let event;
    console.log(type);
    console.log(time.slice(-2));

    /// event form validations
    if (!(time.slice(1, 2) === ":" || time.slice(2, 3) === ":"))
      return alert("Please enter the time in the required format"); //// validating pos of :
    const ampm = time.slice(-2);
    if (!(ampm === "am" || ampm === "pm"))
      return alert("Please enter the time in the required format"); /// validating am / pm
    const ind = time.indexOf(":");
    // console.log(ind);
    const hr = +time.slice(0, ind);
    // console.log(hr);
    const min = +time.slice(ind + 1, -2);
    // console.log(min);
    if (hr > 12 || min > 60) return alert("Please enter a valid time");
    if (!Number.isFinite(fee)) return alert("Fee has to be positive number!");

    if (type === "all") {
      event = new All([lat, lng], location, date, time);
    }

    if (type === "knockout") {
      event = new Knockout([lat, lng], location, date, time);
    }

    this.#events.push(event);
    console.log(event);

    //Render event on map as marker
    this._renderEventMarker(event);

    // Render event on list
    this._renderEvent(event);
    //clear input fields
    this._hideForm();

    //Set local storage to all events
    this._setLocalStorage();
  }

  _renderEventMarker(event) {
    L.marker(event.coords)
      .addTo(this.#map)
      .bindPopup(
        L.popup({
          maxWidth: 250,
          minWidth: 100,
          autoClose: false,
          closeOnClick: false,
          className: `${event.type}-popup`,
        })
      )
      .setPopupContent(
        `${event.type === "all" ? "🏅" : "🥇"} ${event.description}`
      )
      .openPopup();
  }

  _renderEvent(event) {
    const html = `
    <li class = "event event--${event.type}" data-id="${event.id}">
          <h2 class="workout__title">Event type: ${event.type[0].toUpperCase()}${event.type.slice(
      1
    )} @ ${event.location}</h2>
          <div class="workout__details">
            <span class="workout__icon">📅</span>
            <span class="workout__value">${event.date[0].toUpperCase()}${event.date.slice(
      1,
      3
    )} ${event.date.slice(3)}</span>
            
          </div>
          <div class="workout__details">
            <span class="workout__icon">⏱</span>
            <span class="workout__value">${event.time}</span>
            
          </div>`;

    form.insertAdjacentHTML("afterend", html);
  }

  _moveToPopup(e) {
    const eventEl = e.target.closest(".event");

    if (!eventEl) return;

    const event = this.#events.find((ev) => ev.id === eventEl.dataset.id);

    this.#map.setView(event.coords, this.#mapZoomLevel, {
      animate: true,
      pan: {
        duration: 1,
      },
    });
  }

  _setLocalStorage() {
    localStorage.setItem("events", JSON.stringify(this.#events));
  }

  _getLocalStorage() {
    const data = JSON.parse(localStorage.getItem("events"));

    if (!data) return;

    this.#events = data;

    this.#events.forEach((ev) => {
      this._renderEvent(ev);
    });
  }
}

const app = new App();
