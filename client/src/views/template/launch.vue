<template>
  <div class="app-container">
    <el-row>
      <el-card shadow="none">
        <img width="200px" :src="templateData.desc_image">
      </el-card>
    </el-row>
    <el-form ref="form" :model="tempData" :rules="rules">
      <el-form-item label="Name" prop="name">
        <el-input v-model="tempData.name" />
      </el-form-item>

      <el-form-item v-for="(variable, idx) in tempData.variables" :key="idx" :label="variable.key" :required="templateData.user_variables[idx].required">
        <el-input v-model="tempData.variables[idx].value" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="createData">Create</el-button>
      </el-form-item>

    </el-form>

  </div>
</template>

<script>
import { detailTemplate } from '@/api/template'
import { createInstance } from '@/api/instance'

export default {
  data() {
    return {
      rules: {
        name: [
          { required: true, pattern: /^[a-z]+$/
          }
        ]
      },
      templateData: {},
      tempData: {
        name: '',
        variables: []
      }
    }
  },

  created() {
    this.template_id = this.$route.query.template_id
    this.fetchData()
  },
  methods: {
    fetchData() {
      detailTemplate(this.template_id).then(
        response => {
          const { data } = response
          this.templateData = data
          this.tempData.variables = data.user_variables.map(item => {
            return { key: item.key, value: item.default }
          })
          this.tempData.template = data.id
        }
      )
    },
    createData() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          createInstance(this.tempData).then(response => {
            const { data } = response
            this.$notify({
              title: `Instance Create Succeed`,
              type: 'success',
              message: `Instace ${data.name} Create Succeed`
            })
            this.$router.push({ name: 'InstanceList' })
          })
        }
      })
    }
  }
}
</script>
