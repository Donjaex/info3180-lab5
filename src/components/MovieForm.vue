<template>
  <div>
    <!-- Success Message -->
    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>

    <!-- Error Messages -->
    <div v-if="errors.length > 0" class="alert alert-danger">
      <ul>
        <li v-for="error in errors" :key="error">{{ error }}</li>
      </ul>
    </div>

    <form id="movieForm" @submit.prevent="saveMovie">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" name="title" class="form-control" />
      </div>

      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea name="description" class="form-control"></textarea>
      </div>

      <div class="form-group mb-3">
        <label for="poster" class="form-label">Movie Poster</label>
        <input type="file" name="poster" class="form-control" />
      </div>

      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

let csrf_token     = ref('')
let successMessage = ref('')
let errors         = ref([])

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then(response => response.json())
    .then(data => {
      csrf_token.value = data.csrf_token
    })
}

function saveMovie() {
  let movieForm = document.getElementById('movieForm')
  let form_data = new FormData(movieForm)

  fetch('/api/v1/movies', {
    method: 'POST',
    body: form_data,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.errors) {
      errors.value = data.errors
      successMessage.value = ''
    } else {
      successMessage.value = `"${data.title}" added successfully!`
      errors.value = []
    }
  })
  .catch(error => console.log(error))
}

onMounted(() => {
  getCsrfToken()
})
</script>