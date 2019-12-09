<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button class="filter-item" size="mini" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add Template
      </el-button>
    </div>
    <el-dialog fullscreen :title="dialogStatus == 'create' ? 'Create Template': 'Update Template'" :visible.sync="dialogVisible">
      <el-form ref="dataForm" :model="tempData" :rules="rules">
        <el-form-item label="Template Name" prop="name">
          <el-input v-model="tempData.name" autocomplete="off" :disabled="dialogStatus === 'update'" />
        </el-form-item>
        <el-form-item label="Desc Image" prop="desc_image">
          <vue-base64-file-upload
            class="v1"
            accept="image/png"
            image-class="image-preview"
            input-class="v1-image"
            :max-size="customImageMaxSize"
            :default-preview="tempData.desc_image"
            @size-exceeded="onSizeExceeded"
            @file="onFile"
            @load="onLoad"
          />
        </el-form-item>

        <el-form-item label="Providers" prop="providers">
          <el-select v-model="tempData.providers" multiple :disabled="dialogStatus === 'update'">
            <el-option
              v-for="provider in providers"
              :key="provider.name"
              :label="provider.name"
              :value="provider.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Resources" prop="resources">
          <el-input v-model="tempData.resources" type="textarea" autosize :disabled="dialogStatus === 'update'" />
        </el-form-item>
        <el-form-item label="Outputs" prop="outputs">
          <el-input v-model="tempData.outputs" type="textarea" autosize :disabled="dialogStatus === 'update'" />
        </el-form-item>
        <el-form-item label="Variables" prop="varaibles">
          <el-input v-model="tempData.variables" type="textarea" autosize :disabled="dialogStatus === 'update'" />
        </el-form-item>
        <el-form-item label="Datasources" prop="datasources">
          <el-input v-model="tempData.datasources" type="textarea" autosize :disabled="dialogStatus === 'update'" />
        </el-form-item>
        <el-form-item
          v-for="(variable, index) in tempData.user_variables"
          :key="index"
          :label="'User Variable ' + index"
          :prop="'user_variables.' + index"
        >
          <el-row :gutter="10">
            <el-col :span="6">
              <el-input v-model="variable.key" placeholder="key" />
            </el-col>
            <el-col :span="6">
              <el-input v-model="variable.default" placeholder="default value" />
            </el-col>
            <el-col :span="4">
              <span>required</span>
              <el-switch v-model="variable.required" />
            </el-col>
            <el-button size="mini" @click.prevent="removeUserVariable(index)">删除</el-button>
          </el-row>
        </el-form-item>
        <el-form-item>
          <el-button size="mini" @click="addUserVariable()">Add User Variable</el-button>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogStatus === 'create' ? createData() : updateData()">Confirm</el-button>
      </div>
    </el-dialog>

    <el-table
      v-loading="listLoading"
      :data="list"
      style="width: 100%"
    >
      <el-table-column type="expand">
        <template slot-scope="scope">
          <el-form label-position="left" inline class="demo-table-expand">
            <template v-for="config in ['resources', 'variables', 'outputs', 'datasources']">
              <h4>{{ config }}</h4>
              <pre :key="config" style="color: #92a2b3;">{{ scope.row[config] }}</pre>
              <el-divider />
            </template>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        label="Name"
      >
        <template slot-scope="scope">
          <el-tag size="medium">{{ scope.row.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="Providers"
      >
        <template slot-scope="scope">
          <el-tag v-for="provider in scope.row.providers_mapping" :key="provider" size="medium" type="success">{{ provider.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column>
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="handleClone(scope.row)"
          >Clone</el-button>
          <el-button
            size="mini"
            @click="handleEdit(scope.row)"
          >Edit</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.row)"
          >Destroy</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style>
.image-preview {
  height: 400px;
  max-width: 400px;
}
</style>
<script>
import VueBase64FileUpload from 'vue-base64-file-upload'

import { listTemplate, updateTemplate, createTemplate, destroyTemplate } from '@/api/template'
import { listProvider } from '@/api/provider'
import { Loading } from 'element-ui'

export default {
  components: {
    VueBase64FileUpload
  },
  data() {
    return {
      list: [],
      providers: [],
      dialogVisible: false,
      dialogStatus: 'create',
      customImageMaxSize: 0.5,
      listLoading: true,
      tempData: {
        name: '',
        resources: '',
        desc_image: '',
        outputs: '',
        datasources: '',
        variables: '',
        user_variables: []
      },
      rules: {
        name: [
          { required: true, message: 'Please input template name', trigger: 'blur' },
          { min: 2, max: 50, message: 'The length ranges from 3 to 50 character', trigger: 'blur' }
        ],
        desc_image: [
          { required: true, message: 'Please upload template desc image', trigger: 'blur' }
        ],
        providers: [
          { required: true, message: 'Please select provider', trigger: 'blur' }
        ],
        resources: [
          { required: true, message: 'Please input resources', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.fetchData()
    listProvider().then(response => {
      this.providers = response.data
    })
  },
  methods: {
    resetTemp() {
      this.tempData = {
        name: '',
        resources: '',
        outputs: '',
        desc_image: '',
        datasources: '',
        variables: '',
        user_variables: []
      }
    },
    fetchData() {
      listTemplate().then(response => {
        this.list = response.data.map(function(item) {
          item.providers_mapping = Object.assign([], item.providers)
          item.providers = item.providers.map(item => item.id)
          return item
        })
        this.listLoading = false
      })
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogStatus = 'update'
      this.tempData = Object.assign({}, row)
      this.dialogVisible = true
    },
    handleClone(row) {
      this.dialogStatus = 'create'
      this.tempData = Object.assign({}, row)
      this.tempData.desc_image = null
      this.tempData.name += ' Clone'
      this.dialogVisible = true
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const loadingInstance1 = Loading.service({ fullscreen: true, text: 'Validating Template' })
          createTemplate(this.tempData).then(
            response => {
              const { data } = response
              this.$notify({
                title: `Template Create Succeed`,
                type: 'success',
                message: `Template ${data.name} Create Succeed`
              })
              this.dialogVisible = false
              this.fetchData()
              loadingInstance1.close()
            }
          ).catch(error => {
            console.log(error)
            loadingInstance1.close()
          })
        }
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          updateTemplate(this.tempData.id, this.tempData).then(
            response => {
              const { data } = response
              this.$notify({
                title: `Template Update Succeed`,
                type: 'success',
                message: `Template ${data.name} Update Succeed`
              })
              this.dialogVisible = false
            }
          )
        }
      })
    },

    handleDelete(row) {
      destroyTemplate(row.id).then(response => {
        this.fetchData()
      })
    },
    removeUserVariable(idx) {
      this.tempData.user_variables.splice(idx, 1)
    },
    onFile(file) {
      console.log(file) // file object
    },
    onLoad(dataUri) {
      this.tempData.desc_image = dataUri
    },
    onSizeExceeded(size) {
      alert(`Image ${size}Mb size exceeds limits of ${this.customImageMaxSize}Mb!`)
    },
    addUserVariable() {
      this.tempData.user_variables.push({
        key: '',
        required: false,
        default: ''
      })
    }
  }
}
</script>
