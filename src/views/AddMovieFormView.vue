<template>
  <div class="container mt-4">
    <h2>Add Movie</h2>

    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>

    <div v-if="errors.length > 0" class="alert alert-danger">
      <ul class="mb-0">
        <li v-for="(error, i) in errors" :key="i">{{ error }}</li>
      </ul>
    </div>

    <form id="movieForm" @submit.prevent="saveMovie">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" id="title" name="title" class="form-control" />
      </div>

      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea id="description" name="description" class="form-control"></textarea>
      </div>

      <div class="form-group mb-3">
        <label for="poster" class="form-label">Poster</label>
        <input type="file" id="poster" name="poster" class="form-control" />
      </div>

      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");
let successMessage = ref("");
let errors = ref([]);

function getCsrfToken() {
  fetch("/api/v1/csrf-token")
    .then((response) => response.json())
    .then((data) => {
      console.log("CSRF token:", data);
      csrf_token.value = data.csrf_token;
    })
    .catch((error) => {
      console.log("CSRF error:", error);
      errors.value = ["Could not load CSRF token."];
    });
}

function saveMovie() {
  alert("submit fired");
  console.log("submit fired");

  errors.value = [];
  successMessage.value = "";

  const movieForm = document.getElementById("movieForm");
  const form_data = new FormData(movieForm);

  fetch("/api/v1/movies", {
    method: "POST",
    body: form_data,
    headers: {
      "X-CSRFToken": csrf_token.value
    }
  })
    .then(async (response) => {
      const text = await response.text();
      console.log("status:", response.status);
      console.log("raw text:", text);

      let data;
      try {
        data = JSON.parse(text);
      } catch (e) {
        errors.value = ["Server did not return valid JSON."];
        return;
      }

      if (response.ok && data.message) {
        successMessage.value = data.message;
        movieForm.reset();
      } else if (data.errors) {
        errors.value = data.errors;
      } else {
        errors.value = ["Something went wrong."];
      }
    })
    .catch((error) => {
      console.log("submit error:", error);
      errors.value = ["Unable to submit form."];
    });
}

onMounted(() => {
  getCsrfToken();
});
</script>