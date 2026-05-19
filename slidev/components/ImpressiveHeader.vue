<template>
  <div
    class="w-full h-full bg-white text-gray-800 font-sans flex flex-col relative"
  >
    <!-- Header Section -->
    <header class="w-full pt-2.5 px-6 flex flex-col bg-white z-10 relative">
      <!-- Main Header -->
      <h1
        class="text-5xl font-black m-0 tracking-tight leading-none pb-0 text-transparent bg-clip-text bg-gradient-to-r from-blue-800 to-purple-800"
      >
        <slot name="title">Main Header Title</slot>
      </h1>

      <!-- Impressive Horizontal Lines -->
      <div class="flex flex-col gap-1 mt-[-12px]">
        <div
          class="w-full h-[5px] bg-gradient-to-r from-blue-800 via-purple-800 to-transparent impressive-line"
        ></div>
      </div>

      <!-- Sub Header with line separating content -->
      <div class="flex items-center w-full mt-1 mt-2">
        <h2 class="!text-2xl font-bold text-gray-500 m-0 pr-6">
          <slot name="subtitle">Section Subtitle</slot>
        </h2>
        <!-- The line "behind/below" to separate header and content -->
        <div class="flex-grow h-[1px] bg-gray-300"></div>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="flex-grow px-6 py-3 overflow-auto relative z-10 text-[12px]">
      <slot />
    </main>

    <!-- Footer separator & Footer -->
    <div class="w-full px-6">
      <!-- Upper line to separate footer from content -->
      <div class="w-full h-[1px] bg-gray-300"></div>
    </div>
    <footer
      class="w-full px-6 py-2 bg-white flex justify-between items-center z-10 relative"
    >
      <div
        class="text-gray-400 text-[10px] font-semibold tracking-widest uppercase flex items-center gap-1.5"
      >
        <span>Vualidon.FP</span>
        <span class="text-gray-300">|</span>
        <slot name="footer-left">Bao cao phan tich</slot>
      </div>
      <div class="text-gray-400 text-[10px] font-medium">
        <SlideCurrentNo /> / <SlidesTotal />
      </div>
    </footer>
  </div>
</template>

<style scoped>
div.bg-white {
  position: absolute;
  inset: 0;
}
h1 {
  font-size: 30px !important;
  background: linear-gradient(to right, #1e40af, #6b21a8) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
}
.impressive-line {
  background: linear-gradient(
    to right,
    #1e40af 0%,
    #6b21a8 70%,
    rgba(107, 33, 168, 0) 100%
  ) !important;
}
h2 {
  font-size: 14px !important;
}
h2 :deep(p) {
  margin: 0;
  display: inline;
  font-size: inherit;
  color: inherit;
  font-weight: inherit;
  text-transform: inherit;
  letter-spacing: inherit;
}
main,
main :deep(p),
main :deep(span),
main :deep(li),
main :deep(div),
main :deep(td),
main :deep(th) {
  font-size: 12px !important;
}
footer,
footer :deep(div),
footer :deep(span) {
  font-size: 10px !important;
}
</style>
