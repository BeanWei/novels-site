<template>
  <div id="login">
    <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="80">
      <FormItem label="Email" prop="email">
        <Input type="email" v-model="formCustom.email">
          <Icon type="email" slot="prepend"></Icon>
        </Input>
      </FormItem>
      <FormItem label="Password" prop="passwd">
        <Input type="password" v-model="formCustom.passwd">
          <Icon type="locked" slot="prepend"></Icon>
        </Input>
      </FormItem>
      <FormItem label="Confirm" prop="passwdCheck">
        <Input type="password" v-model="formCustom.passwdCheck">
          <Icon type="locked" slot="prepend"></Icon>
        </Input>
      </FormItem>
      <FormItem label="Code" prop="code">
        <Input type="text" v-model="formCustom.code" number>
          <Icon type="paper-airplane" slot="prepend"></Icon>
        </Input>
      </FormItem>
      <FormItem>
        <Button type="primary" @click="handleSubmit('formCustom')">Submit</Button>
        <Button type="ghost" @click="handleReset('formCustom')" style="margin-left: 8px">Reset</Button>
      </FormItem>
    </Form>
  </div>
</template>
<script>
  export default {
    data () {
      const validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('Please enter your password'));
        } else {
        if (this.formCustom.passwdCheck !== '') {
          // 对第二个密码框单独验证
          this.$refs.formCustom.validateField('passwdCheck');
        }
        callback();
        }
      };
      const validatePassCheck = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('Please enter your password again'));
        } else if (value !== this.formCustom.passwd) {
          callback(new Error('The two input passwords do not match!'));
        } else {
          callback();
        }
      };
      const validateAge = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('Age cannot be empty'));
        }
        // 模拟异步验证效果
        setTimeout(() => {
          if (!Number.isInteger(value)) {
            callback(new Error('Please enter a numeric value'));
            } else {
              if (value < 18) {
                callback(new Error('Must be over 18 years ofcode'));
                } else {
                  callback();
                }
              }
            }, 1000);
      }; 
      return {
        formCustom: {
          passwd: '',
          passwdCheck: '',
          code: ''
        },
        ruleCustom: {
          passwd: [
            { validator: validatePass, trigger: 'blur' }
          ],
          passwdCheck: [
            { validator: validatePassCheck, trigger: 'blur' }
          ],
          code: [
            { validator: validateAge, trigger: 'blur' }
          ]
        }
      }
   },
    methods: {
      handleSubmit (name) {
        this.$refs[name].validate((valid) => {
          if (valid) {
            this.$Message.success('Success!');
          } else {
            this.$Message.error('Fail!');
          }
        })
      },
      handleReset (name) {
        this.$refs[name].resetFields();
      }
    }
  }
</script>

<style scoped>
  #login {
    width: 400px;
    margin: 50px auto;
  }
</style>
