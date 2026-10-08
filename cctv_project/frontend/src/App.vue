<template>
  <div class="container">
    <!-- Ошибки API -->
    <div v-if="errorMessage" class="error-banner">
      <span>⚠️ {{ errorMessage }}</span>
      <button class="icon-btn" @click="errorMessage = ''">✕</button>
    </div>

    <!-- Верхний блок: Таблица и Форма (по макету) -->
    <div class="top-grid">
      <!-- Список источников -->
      <div class="window-card">
        <div class="window-header">Управление камерами</div>
        <div class="window-body">
          <h2 class="section-title">Источники видео</h2>
          
          <div class="toolbar">
            <input 
              v-model="searchQuery" 
              @input="fetchSources" 
              type="text" 
              class="search-input" 
              placeholder="Поиск по названию / location" 
            />
            <button class="btn btn-green" @click="resetFormForCreate">+ Добавить</button>
          </div>

          <table class="sources-table">
            <thead>
              <tr>
                <th>Название</th>
                <th>URL</th>
                <th>Локация</th>
                <th>Статус</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="sources.length === 0">
                <td colspan="5" style="text-align: center; color: #64748b; padding: 20px;">
                  Источники не найдены
                </td>
              </tr>
              <tr 
                v-for="source in sources" 
                :key="source.id"
                @click="selectSource(source)"
                :style="{ cursor: 'pointer', backgroundColor: selectedSource?.id === source.id ? '#f1f5f9' : 'transparent' }"
              >
                <td><strong>{{ source.name }}</strong></td>
                <td style="font-family: monospace; font-size: 13px;">{{ source.url }}</td>
                <td>{{ source.location }}</td>
                <td>
                  <span :style="{ color: source.enabled ? '#16a34a' : '#dc2626', fontWeight: 'bold' }">
                    {{ source.enabled ? 'Включен' : 'Выключен' }}
                  </span>
                </td>
                <td class="actions-cell" @click.stop>
                  <button class="icon-btn" title="Редактировать" @click="editSource(source)">✏️</button>
                  <button class="icon-btn" title="Переключить статус" @click="toggleEnabled(source)">⚡</button>
                  <button class="icon-btn" title="Удалить" @click="confirmDelete(source)">🗑️</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Форма создания/редактирования -->
      <div class="window-card">
        <div class="window-header">Управление камерами</div>
        <div class="window-body">
          <h2 class="section-title">
            {{ isEditing ? 'Редактировать источник' : 'Добавить источник' }}
          </h2>

          <form @submit.prevent="saveSource">
            <div class="form-group">
              <label>Название</label>
              <input 
                v-model="form.name" 
                type="text" 
                class="form-control" 
                placeholder="Конвейер №1" 
                required 
              />
            </div>

            <div class="form-group">
              <label>RTSP URL</label>
              <input 
                v-model="form.url" 
                type="text" 
                class="form-control" 
                placeholder="rtsp://192.168.1.1212/stream" 
                required 
              />
            </div>

            <div class="form-group">
              <label>Локация</label>
              <input 
                v-model="form.location" 
                type="text" 
                class="form-control" 
                placeholder="Цех 3" 
                required 
              />
            </div>

            <div class="form-footer">
              <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-weight: 600; font-size: 14px;">Статус</span>
                <button 
                  type="button" 
                  class="btn" 
                  :class="form.enabled ? 'btn-green' : 'btn-red'"
                  @click="form.enabled = !form.enabled"
                >
                  {{ form.enabled ? 'Включен' : 'Выключен' }}
                </button>
              </div>

              <div style="display: flex; gap: 8px;">
                <button v-if="isEditing" type="button" class="btn btn-blue" @click="resetFormForCreate">
                  Отмена
                </button>
                <button type="submit" class="btn btn-green">Сохранить</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Нижний блок: Карточка выбранного источника (по макету) -->
    <div class="window-card" v-if="selectedSource">
      <div class="window-header">Карточка источника / Редактирование</div>
      <div class="window-body">
        <div class="detail-card-content">
          <div class="detail-info">
            <h1 style="font-size: 24px; margin-bottom: 8px;">{{ selectedSource.name }}</h1>
            <div><strong>ID:</strong> {{ selectedSource.id }}</div>
            <div><strong>RTSP URL:</strong> <span style="font-family: monospace;">{{ selectedSource.url }}</span></div>
            <div><strong>Location:</strong> {{ selectedSource.location }}</div>
            <div><strong>Status:</strong> {{ selectedSource.enabled ? 'Enabled' : 'Disabled' }}</div>
            <div><strong>Created at:</strong> {{ formatDate(selectedSource.created_at) }}</div>
          </div>

          <div class="detail-actions">
            <button class="btn btn-blue" @click="editSource(selectedSource)">Редактировать</button>
            <button 
              class="btn" 
              :class="selectedSource.enabled ? 'btn-yellow' : 'btn-green'"
              @click="toggleEnabled(selectedSource)"
            >
              {{ selectedSource.enabled ? 'Выключить' : 'Включить' }}
            </button>
            <button class="btn btn-red" @click="confirmDelete(selectedSource)">Удалить</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <div v-if="sourceToDelete" class="modal-overlay">
      <div class="modal-content">
        <h3 style="margin-bottom: 12px;">Подтверждение удаления</h3>
        <p style="margin-bottom: 20px;">
          Вы действительно хотите удалить источник <strong>"{{ sourceToDelete.name }}"</strong>?
        </p>
        <div style="display: flex; justify-content: flex-end; gap: 12px;">
          <button class="btn btn-blue" @click="sourceToDelete = null">Отмена</button>
          <button class="btn btn-red" @click="deleteSource">Удалить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = '/sources'

const sources = ref([])
const searchQuery = ref('')
const selectedSource = ref(null)
const sourceToDelete = ref(null)
const errorMessage = ref('')
const isEditing = ref(false)

const form = ref({
  id: null,
  name: '',
  url: '',
  location: '',
  enabled: true
})

const fetchSources = async () => {
  try {
    errorMessage.value = ''
    const res = await axios.get(API_BASE, {
      params: { search: searchQuery.value || undefined }
    })
    sources.value = res.data
    if (selectedSource.value) {
      const updated = sources.value.find(s => s.id === selectedSource.value.id)
      selectedSource.value = updated || null
    }
  } catch (err) {
    handleError(err)
  }
}

const selectSource = (source) => {
  selectedSource.value = source
}

const resetFormForCreate = () => {
  isEditing.value = false
  form.value = {
    id: null,
    name: '',
    url: '',
    location: '',
    enabled: true
  }
}

const editSource = (source) => {
  isEditing.value = true
  form.value = {
    id: source.id,
    name: source.name,
    url: source.url,
    location: source.location,
    enabled: source.enabled
  }
  selectedSource.value = source
}

const saveSource = async () => {
  try {
    errorMessage.value = ''
    if (isEditing.value && form.value.id) {
      await axios.patch(`${API_BASE}/${form.value.id}`, {
        name: form.value.name,
        url: form.value.url,
        location: form.value.location,
        enabled: form.value.enabled
      })
    } else {
      const res = await axios.post(API_BASE, {
        name: form.value.name,
        url: form.value.url,
        location: form.value.location,
        enabled: form.value.enabled
      })
      selectedSource.value = res.data
    }
    await fetchSources()
    resetFormForCreate()
  } catch (err) {
    handleError(err)
  }
}

const toggleEnabled = async (source) => {
  try {
    errorMessage.value = ''
    await axios.patch(`${API_BASE}/${source.id}`, {
      enabled: !source.enabled
    })
    await fetchSources()
  } catch (err) {
    handleError(err)
  }
}

const confirmDelete = (source) => {
  sourceToDelete.value = source
}

const deleteSource = async () => {
  if (!sourceToDelete.value) return
  try {
    errorMessage.value = ''
    await axios.delete(`${API_BASE}/${sourceToDelete.value.id}`)
    if (selectedSource.value?.id === sourceToDelete.value.id) {
      selectedSource.value = null
    }
    sourceToDelete.value = null
    await fetchSources()
  } catch (err) {
    handleError(err)
  }
}

const handleError = (err) => {
  if (err.response && err.response.data && err.response.data.detail) {
    const detail = err.response.data.detail
    if (Array.isArray(detail)) {
      errorMessage.value = detail.map(d => `${d.loc ? d.loc.join('.') : ''}: ${d.msg}`).join(', ')
    } else {
      errorMessage.value = detail
    }
  } else {
    errorMessage.value = err.message || 'Произошла ошибка запроса к серверу'
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleString('ru-RU', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchSources()
})
</script>