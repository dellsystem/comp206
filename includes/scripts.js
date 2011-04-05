// Please someone clean up my code I'm not used to pure JS

function submitRoom(roomID) {
    var room_field = document.forms['rooms'].elements["room"];
    room_field.value = roomID;
    document.rooms.submit();
}
