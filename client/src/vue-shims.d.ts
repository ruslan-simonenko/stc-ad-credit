// According to https://github.com/vuejs/vue/issues/5298#issuecomment-970689689
declare module '*.vue' {
    import {DefineComponent} from 'vue';
    const component: DefineComponent<{}, {}, any>;
    export default component;
}

