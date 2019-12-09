<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button class="filter-item" size="mini" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add Provider
      </el-button>
    </div>
    <el-dialog :title="dialogStatus == 'create' ? 'Create Provider': 'Update Provider'" :visible.sync="dialogVisible">
      <el-form ref="form" :model="tempData" label-width="80px">
        <el-form-item label="Provider Name" prop="name" required>
          <el-input v-model="tempData.name" />
        </el-form-item>

        <el-form-item label="Config" prop="config" required>
          <el-input v-model="tempData.config" type="textarea" autosize />
        </el-form-item>

        <el-form-item label="Tags" prop="tags">
          <el-tag
            v-for="tag in tempData.tags"
            :key="tag"
            closable
            :disable-transitions="false"
            @close="handleClose(tag)"
          >
            {{ tag }}
          </el-tag>
          <el-input
            v-if="inputVisible"
            ref="saveTagInput"
            v-model="inputValue"
            class="input-new-tag"
            size="small"
            @keyup.enter.native="handleInputConfirm"
            @blur="handleInputConfirm"
          />
          <el-button v-else class="button-new-tag" size="small" @click="showInput">+ New Tag</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="dialogStatus === 'create' ? createData(): updateData()">Confirm</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <el-table
      :data="list"
      style="width: 100%"
    >
      <el-table-column type="expand">
        <template slot-scope="scope">
          <el-form label-position="left" inline class="demo-table-expand">
            <pre>{{ scope.row.config }}</pre>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        label="Name"
        width="180"
      >
        <template slot-scope="scope">
          <el-tag size="medium">{{ scope.row.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="Tags"
        width="180"
      >
        <template slot-scope="scope">
          <el-tag v-for="tag in scope.row.tags" :key="tag" size="medium" type="success">{{ tag }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column>
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="handleEdit(scope.row)"
          >编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style>
  .el-tag + .el-tag {
    margin-left: 10px;
  }
  .button-new-tag {
    margin-left: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }
  .input-new-tag {
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
  }
</style>

<script>
import { listProvider, createProvider, updateProvider, destroyProvider } from '@/api/provider'
export default {
  data() {
    return {
      list: [],
      tempData: {
        config: null,
        name: null,
        tags: []
      },
      dialogVisible: false,
      inputVisible: false,
      inputValue: '',
      dialogStatus: 'create'
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    resetTemp() {
      this.tempData = {
        config: null,
        name: null,
        tags: []
      }
    },
    handleClose(tag) {
      this.tempData.tags.splice(this.tempData.tags.indexOf(tag), 1)
    },

    showInput() {
      this.inputVisible = true
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus()
      })
    },

    handleInputConfirm() {
      const inputValue = this.inputValue
      if (inputValue) {
        this.tempData.tags.push(inputValue)
      }
      this.inputVisible = false
      this.inputValue = ''
    },
    fetchData() {
      listProvider().then(response => {
        this.list = response.data
      })
    },
    handleEdit(row) {
      this.tempData = Object.assign({}, row)
      this.dialogStatus = 'update'
      this.dialogVisible = true
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogVisible = true
    },
    handleDelete(row) {
      destroyProvider(row.id).then(response => {
        this.fetchData()
      })
    },
    createData() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          createProvider(this.tempData).then(
            response => {
              this.dialogVisible = false
              this.fetchData()
            }
          )
        }
      }
      )
    },
    updateData() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          updateProvider(this.tempData.id, this.tempData).then(
            response => {
              this.dialogVisible = false
              this.fetchData()
            }
          )
        }
      }
      )
    }
  }
}
</script>
