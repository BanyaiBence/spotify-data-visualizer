
// Function to open the modal
function openModal(albumName, albumImage, albumUrl, tracks) {
const modal = document.getElementById('albumModal');
const modalBody = modal.querySelector('.modal-body');

// Dynamically populate modal content
modalBody.querySelector('h2').innerText = albumName;
modalBody.querySelector('img').src = albumImage;
modalBody.querySelector('a').href = albumUrl;
const tracklist = modalBody.querySelector('ul');

tracklist.innerHTML = '';
tracks.forEach(track => {
    const li = document.createElement('li');
    li.innerText = track;
    tracklist.appendChild(li);
});

// Show the modal
modal.style.display = "block";
}

// Function to close the modal
function closeModal() {
const modal = document.getElementById('albumModal');
modal.style.display = "none";
}

// Event listener to close modal when the close button is clicked
document.querySelector('.close-btn').addEventListener('click', closeModal);

// Close modal if the user clicks outside the modal content
window.onclick = function(event) {
const modal = document.getElementById('albumModal');
if (event.target === modal) {
    closeModal();
}
}
