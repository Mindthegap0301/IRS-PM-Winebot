<template>
  <transition name="fade">
    <div class="loading__wrapper">
      <div class="loading__container">
        <div class="loading__loader"></div>
        <div class="loading__loader"></div>
        <div class="loading__loader"></div>
      </div>
      <div class="loading__label">Loading...</div>
    </div>
  </transition>
</template>

<style>
.loading__wrapper {
  --height: 1rem;
}

.loading__wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
}

.loading__container {
  width: 100%;
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  gap: 0.4rem;
}

.loading__loader {
  height: var(--height);
  width: 8rem;
  border-radius: var(--height);
  position: relative;
  overflow: hidden;
}

.loading__loader::after {
  content: "";
  position: absolute;
  width: 10rem;
  height: var(--height);
  border-radius: var(--height);
  /* background: rgb(68, 92, 231);*/
  background: var(--primary-color);
  box-shadow: 0 -0.6rem 0 rgba(220, 100, 160, 0.2) inset;

  animation: slide 4s ease-in-out infinite;
}

.loading__loader:nth-child(2)::after {
  animation-delay: 0.2s;
}

.loading__loader:nth-child(3)::after {
  animation-delay: 0.4s;
}

.loading__label {
  width: 100%;
  text-align: center;
}

@keyframes slide {
  0% {
    left: -7rem;
  }

  50% {
    left: calc(100% - var(--height));
  }

  100% {
    left: -7rem;
  }
}
</style>
