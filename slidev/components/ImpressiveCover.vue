<template>
  <div class="w-full h-full bg-white text-gray-800 font-sans flex flex-col justify-between absolute inset-0">
    
    <!-- Cover Main Section (Left 45%) -->
    <div class="flex flex-col pt-24 px-6 z-10 relative max-w-[45%]">
      <!-- Main Cover Title -->
      <h1 class="text-6xl font-black m-0 tracking-tight leading-tight pb-0 text-transparent bg-clip-text bg-gradient-to-r from-blue-800 to-purple-800">
        <!-- <span name="title" class="!text-[60px]">Vualidon.FP </span> -->
        <span name="title" class="!text-[50px]">Banking Analysis</span>
      </h1>
      
      <!-- Signature Impressive Horizontal Gradient Line -->
      <div class="flex flex-col gap-1 mt-2 mb-4">
        <div class="w-full h-[12px] bg-gradient-to-r from-blue-800 via-purple-800 to-transparent impressive-line"></div>
      </div>
      
      <!-- Subtitle / Report Theme -->
      <h2 class="text-2xl font-bold text-gray-500 m-0 leading-snug">
        <slot name="subtitle">Report Subtitle & Scope</slot>
      </h2>

      <!-- Metadatas (Author, Date, Version) -->
      <div class="mt-8 flex flex-col gap-1 text-[12px] text-gray-400 font-medium">
        <slot name="info">
          <div>Prepared by: Analysis Team</div>
          <div>Date: May 2026</div>
        </slot>
      </div>
    </div>

    <!-- Right Side Bleed Image: occupies absolute right 50% height/width, flat corners, no header/footer -->
    <div v-if="$slots.image" class="absolute right-0 top-0 bottom-0 w-1/2 overflow-hidden z-0 bg-slate-50 cover-image-container">
      <slot name="image" />
    </div>

    <!-- Footer matching the standard header style for absolute brand alignment (Left 45%) -->
    <div class="w-full max-w-[45%] px-6 pb-2 z-10 relative">
      <!-- Upper separator line -->
      <div class="w-full h-[1px] bg-gray-200 mb-2"></div>
      
      <footer class="w-full py-1 bg-white flex justify-between items-center z-10 relative">
        <div class="text-gray-400 text-[10px] font-semibold tracking-widest uppercase flex items-center gap-1.5">
          <span>Vualidon.FP</span>
          <span class="text-gray-300">|</span>
          <slot name="footer-left">Bao cao phan tich</slot>
        </div>
        <!-- Usually no page number on cover, but we keep a subtle indicator -->
        <div class="text-gray-400 text-[10px] font-medium uppercase tracking-wider">
          <slot name="footer-right">Executive Brief</slot>
        </div>
      </footer>
    </div>
    
  </div>
</template>

<style scoped>
h1 {
  font-size: 55px !important;
  background: linear-gradient(to right, #1e40af, #6b21a8) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
}
.impressive-line {
  background: linear-gradient(to right, #1e40af 0%, #6b21a8 70%, rgba(107, 33, 168, 0) 100%) !important;
}
h2 {
  font-size: 20px !important;
}
h2 :deep(p) {
  margin: 0;
  display: inline;
  font-size: inherit;
  color: inherit;
  font-weight: inherit;
}
.cover-image-container :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
