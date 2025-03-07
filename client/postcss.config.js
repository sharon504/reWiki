import tailwindcss from "tailwindcss";
export default {
  plugins: {
    tailwindcss: {
      content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
      theme: {
        extend: {},
      },
      plugins: [tailwindcss],
    },
    autoprefixer: {},
  },
};
