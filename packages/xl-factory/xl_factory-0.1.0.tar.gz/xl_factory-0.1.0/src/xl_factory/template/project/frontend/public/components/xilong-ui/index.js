// const imports = import.meta.globEager("./*.vue");
const imports = import.meta.globEager('./**/*.vue');
export default {
    install(app) {
        for (const path in imports) {
            const component = imports[path];
            const regex = /\.\/\w+\/(\w+)\.vue$/;
            const match = path.match(regex);
            const name = match ? match[1] : null;
            app.component(name, component.default);
        }
    },
};


// import { defineAsyncComponent } from 'vue';
// import { resolveComponent } from '@vue/runtime-core';

// const files = require.context('./XilongUI', true, /\.vue$/);

// export default {
//   install(app) {
//     files.keys().forEach(fileName => {
//       const componentConfig = files(fileName);
//       const componentName = resolveComponent(fileName);
//       const component = defineAsyncComponent(() => componentConfig);
//       app.component(componentName, component);
//     });
//   },
// };




// import { defineAsyncComponent } from 'vue';
// import { resolveComponent } from '@vue/runtime-core';

// const files = import.meta.globEager('./**/*.vue');

// export default {
//     install(app) {
//         for (const path in files) {
//             const componentConfig = files[path];
//             const componentPath = resolveComponent(path);
//             const regex = /\.\/\w+\/(\w+)\.vue$/;
//             const match = componentPath.match(regex);
//             const componentName = match ? match[1] : null;
//             console.log(componentName); // 输出 "ZFlexTable"


//             const component = defineAsyncComponent(() => componentConfig);
//             app.component(componentName, component);
//         }
//     },
// };