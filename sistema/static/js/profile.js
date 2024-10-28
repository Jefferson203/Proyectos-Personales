function changeProfilePicture(event) {
    const fileInput = event.target;
    const profilePicture = document.getElementById('profile-picture');
  
    const file = fileInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        profilePicture.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }
  