<template>
  <div>
    <Form
      :model="formState"
      :label-col="{ span: 8 }"
      :wrapper-col="{ span: 16 }"
      autocomplete="off"
      @finish="onFinish"
      @finishFailed="onFinishFailed"
    >
      <FormItem
        label="Email"
        name="email"
        :rules="[{ required: true, message: 'Please input your email!' }]"
      >
        <Input type="email" v-model:value="formState.email" />
      </FormItem>

      <FormItem
        label="Password"
        name="password"
        :rules="[{ required: true, message: 'Please input your password!' }]"
      >
        <InputPassword v-model:value="formState.password" />
      </FormItem>

      <FormItem :wrapper-col="{ offset: 0, span: 24 }">
        <Button type="primary" :block="true" html-type="submit">Login</Button>
      </FormItem>
    </Form>
  </div>
</template>

<script>
import { ref } from "vue";
import { Button, Form, FormItem, Input, InputPassword } from "ant-design-vue";

export default {
  components: {
    Form,
    FormItem,
    Input,
    Button,
    InputPassword,
  },
  setup(props, { emit }) {
    const formState = ref({
      email: "",
      password: "",
    });

    const onFinishFailed = () => {};

    return {
      formState,
      onFinish(values) {
        emit("submitLogin", values);
      },
      onFinishFailed,
    };
  },
};
</script>
