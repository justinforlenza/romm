<script setup lang="ts">
import romApi from "@/services/api/rom";
import storeAuth from "@/stores/auth";
import type { DetailedRom } from "@/stores/roms";
import type { RomUserStatus } from "@/__generated__";
import { getTextForStatus, getEmojiForStatus } from "@/utils";
import { MdEditor, MdPreview } from "md-editor-v3";
import "md-editor-v3/lib/style.css";
import { ref, watch } from "vue";
import { useDisplay, useTheme } from "vuetify";
import { useI18n } from "vue-i18n";
import { storeToRefs } from "pinia";

// Props
const { t } = useI18n();
const props = defineProps<{ rom: DetailedRom }>();
const auth = storeAuth();
const theme = useTheme();
const { mdAndUp, smAndDown } = useDisplay();
const { scopes } = storeToRefs(auth);
const editingNote = ref(false);
const romUser = ref(props.rom.rom_user);
const publicNotes =
  props.rom.user_notes?.filter((note) => note.user_id !== auth.user?.id) ?? [];

const statusOptions = [
  "never_playing",
  "retired",
  "incomplete",
  "finished",
  "completed_100",
];

// Functions
function editNote() {
  if (editingNote.value) {
    romApi.updateUserRomProps({
      romId: props.rom.id,
      data: romUser.value,
    });
  }
  editingNote.value = !editingNote.value;
}

function onStatusItemClick(status: string | null) {
  romUser.value.status = status as RomUserStatus | null;
}

watch(
  () => props.rom,
  async () => (romUser.value = props.rom.rom_user),
);

watch(
  romUser,
  () => {
    if (scopes.value.includes("roms.user.write")) {
      romApi.updateUserRomProps({
        romId: props.rom.id,
        data: romUser.value,
      });
    }
  },
  { deep: true },
);
</script>

<template>
  <v-card class="mb-2">
    <v-card-title class="bg-toplayer">
      <v-list-item class="pl-2 pr-0">
        <span class="text-h6">{{ t("rom.status") }}</span>
      </v-list-item>
    </v-card-title>
    <v-card-text class="px-8 py-4">
      <v-row
        class="align-center"
        :class="{ 'text-center': smAndDown }"
        no-gutters
      >
        <v-col cols="12" md="5">
          <v-checkbox
            :disabled="!scopes.includes('roms.user.write')"
            v-model="romUser.backlogged"
            color="primary"
            hide-details
          >
            <template #label
              ><span>{{ t("rom.backlogged") }}</span
              ><span class="ml-2">{{
                getEmojiForStatus("backlogged")
              }}</span></template
            >
          </v-checkbox>
          <v-checkbox
            :disabled="!scopes.includes('roms.user.write')"
            v-model="romUser.now_playing"
            color="primary"
            hide-details
          >
            <template #label
              ><span>{{ t("rom.now-playing") }}</span
              ><span class="ml-2">{{
                getEmojiForStatus("now_playing")
              }}</span></template
            >
          </v-checkbox>
          <v-checkbox
            :disabled="!scopes.includes('roms.user.write')"
            v-model="romUser.hidden"
            color="primary"
            hide-details
          >
            <template #label
              ><span>{{ t("rom.hidden") }}</span
              ><span class="ml-2">{{
                getEmojiForStatus("hidden")
              }}</span></template
            >
          </v-checkbox>
        </v-col>
        <v-col cols="12" md="7">
          <v-row
            class="d-flex align-center"
            :class="{ 'mt-4': smAndDown }"
            no-gutters
          >
            <v-col cols="12" md="2">
              <v-label>{{ t("rom.rating") }}</v-label>
            </v-col>
            <v-col cols="12" md="10">
              <v-rating
                :class="{ 'ml-2': mdAndUp }"
                hover
                ripple
                length="10"
                size="26"
                :disabled="!scopes.includes('roms.user.write')"
                v-model="romUser.rating"
                @update:model-value="
                  romUser.rating =
                    typeof $event === 'number' ? $event : parseInt($event)
                "
                active-color="yellow"
              />
            </v-col>
          </v-row>
          <v-row class="d-flex align-center mt-4" no-gutters>
            <v-col cols="12" md="2">
              <v-label>{{ t("rom.difficulty") }}</v-label>
            </v-col>
            <v-col cols="12" md="10">
              <v-rating
                :class="{ 'ml-2': mdAndUp }"
                hover
                ripple
                length="10"
                size="26"
                :disabled="!scopes.includes('roms.user.write')"
                full-icon="mdi-chili-mild"
                empty-icon="mdi-chili-mild-outline"
                v-model="romUser.difficulty"
                @update:model-value="
                  romUser.difficulty =
                    typeof $event === 'number' ? $event : parseInt($event)
                "
                active-color="red"
              />
            </v-col>
          </v-row>
          <v-row class="d-flex align-center mt-4" no-gutters>
            <v-col cols="12" md="2">
              <v-label>{{ t("rom.completion") }} %</v-label>
            </v-col>
            <v-col cols="12" md="10">
              <v-slider
                :class="{ 'ml-4': mdAndUp }"
                :disabled="!scopes.includes('roms.user.write')"
                v-model="romUser.completion"
                min="1"
                max="100"
                step="1"
                hide-details
                track-fill-color="primary"
                ><template #append>
                  <v-label class="ml-2 opacity-100">
                    {{ romUser.completion }}%
                  </v-label>
                </template></v-slider
              >
            </v-col>
          </v-row>
          <div class="d-flex align-center mt-4">
            <v-select
              :disabled="!scopes.includes('roms.user.write')"
              v-model="romUser.status"
              :items="statusOptions"
              hide-details
              :label="t('rom.status')"
              clearable
              variant="outlined"
              density="compact"
              class="mt-1"
            >
              <template #selection="{ item }">
                <span>{{ getEmojiForStatus(item.raw as RomUserStatus) }}</span
                ><span class="ml-2">{{
                  getTextForStatus(item.raw as RomUserStatus)
                }}</span>
              </template>
              <template #item="{ item }">
                <v-list-item link @click="onStatusItemClick(item.raw)">
                  <span>{{ getEmojiForStatus(item.raw as RomUserStatus) }}</span
                  ><span class="ml-2">{{
                    getTextForStatus(item.raw as RomUserStatus)
                  }}</span>
                </v-list-item>
              </template>
            </v-select>
          </div>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>

  <v-card>
    <v-card-title class="bg-toplayer">
      <v-list-item class="pl-2 pr-0">
        <span class="text-h6">{{ t("rom.my-notes") }}</span>
        <template #append>
          <v-btn-group divided density="compact">
            <v-tooltip
              location="top"
              class="tooltip"
              transition="fade-transition"
              :text="romUser.note_is_public ? 'Make private' : 'Make public'"
              open-delay="500"
              ><template #activator="{ props: tooltipProps }">
                <v-btn
                  :disabled="!scopes.includes('roms.user.write')"
                  @click="romUser.note_is_public = !romUser.note_is_public"
                  v-bind="tooltipProps"
                  class="bg-toplayer"
                >
                  <v-icon size="large">
                    {{ romUser.note_is_public ? "mdi-eye" : "mdi-eye-off" }}
                  </v-icon>
                </v-btn>
              </template></v-tooltip
            >
            <v-tooltip
              location="top"
              class="tooltip"
              transition="fade-transition"
              text="Edit note"
              open-delay="500"
              ><template #activator="{ props: tooltipProps }">
                <v-btn
                  :disabled="!scopes.includes('roms.user.write')"
                  @click="editNote"
                  v-bind="tooltipProps"
                  class="bg-toplayer"
                >
                  <v-icon size="large">
                    {{ editingNote ? "mdi-check" : "mdi-pencil" }}
                  </v-icon>
                </v-btn>
              </template></v-tooltip
            >
          </v-btn-group>
        </template>
      </v-list-item>
    </v-card-title>
    <v-card-text class="pa-2">
      <MdEditor
        v-if="editingNote"
        :disabled="!scopes.includes('roms.user.write')"
        v-model="romUser.note_raw_markdown"
        :theme="theme.name.value == 'dark' ? 'dark' : 'light'"
        language="en-US"
        :preview="false"
        :no-upload-img="true"
        class="editor-preview"
      />
      <MdPreview
        v-else
        :model-value="romUser.note_raw_markdown"
        :theme="theme.name.value == 'dark' ? 'dark' : 'light'"
        preview-theme="vuepress"
        code-theme="github"
      />
    </v-card-text>
  </v-card>

  <v-card v-if="publicNotes && publicNotes.length > 0" class="mt-2">
    <v-card-title class="bg-toplayer">
      <v-list-item class="pl-2 pr-0">
        <span class="text-h6">{{ t("rom.public-notes") }}</span>
      </v-list-item>
    </v-card-title>

    <v-divider />

    <v-card-text class="pa-0">
      <v-expansion-panels multiple flat variant="accordion">
        <v-expansion-panel v-for="note in publicNotes">
          <v-expansion-panel-title class="bg-toplayer">
            <span class="text-body-1">{{ note.username }}</span>
          </v-expansion-panel-title>
          <v-expansion-panel-text class="bg-surface">
            <MdPreview
              :model-value="note.note_raw_markdown"
              :theme="theme.name.value == 'dark' ? 'dark' : 'light'"
              preview-theme="vuepress"
              code-theme="github"
            />
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card-text>
  </v-card>
</template>

<style>
.md-editor-dark {
  --md-bk-color: #161b22 !important;
}
.md-editor,
.md-editor-preview {
  word-break: break-word !important;
  line-height: 1.25 !important;
}
.vuepress-theme pre code {
  background-color: #0d1117;
}
.v-expansion-panel-text__wrapper {
  padding: 0px !important;
}
</style>
