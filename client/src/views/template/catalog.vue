<template>
  <div class="app-container">
    <el-row>
      <vue-element-loading :active="listLoading" spinner="bar-fade-scale" color="#FF6700" text="wait loading" />
      <el-col v-for="template in list" :key="template.id" :span="6">
        <el-card style="margin: 10px" shadow="hover">
          <img style="padding: 0px; height: 150px" :src="template.desc_image" class="image">
          <el-divider />
          <div style="padding: 14px">
            <span>{{ template.name }}</span>
            <div class="bottom clearfix">
              <el-button type="text" @click="handleDeploy(template.id)">Deploy</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style>
  .time {
    font-size: 13px;
    color: #999;
  }

  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }

  .image {
    width: 100%;
    display: block;
  }

  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }

  .clearfix:after {
      clear: both
  }
</style>

<script>
import { listTemplate } from '@/api/template'

export default {
  data() {
    return {
      list: [],
      listLoading: true
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      listTemplate().then(response => {
        this.list = response.data
        this.listLoading = false
      })
    },
    handleDeploy(template_id) {
      this.$router.push({ name: 'TemplateLaunch', query: { template_id: template_id }})
    }
  }
}
</script>
