<template>
  <div class="app-container">
    <div class="filter-container" style="margin-bottom: 18px;">
      <el-input v-model="listQuery.name" placeholder="Name" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.sort" placeholder="By ID" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        Export
      </el-button>
      <el-checkbox v-model="showReviewer" class="filter-item" style="margin-left:15px;" @change="tableKey=tableKey+1">
        reviewer
      </el-checkbox>
    </div>

    <el-table
      ref="multipleTable"
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      :default-sort="{prop: 'id', order: 'ascending'}"
      @sort-change="sortChange"
      @selection-change="handleSelectionChange"
    >
      <el-table-column
        type="selection"
        align="center"
        width="50"
      />
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="60" :class-name="getSortClass('id')">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column type="expand" align="center" width="50" label="详情">
        <template slot-scope="props">
          <el-form label-position="left" class="table-expand">
            <el-form-item label="用例名称">
              <span>{{ props.row.name }}</span>
            </el-form-item>
            <el-form-item label="所属项目">
              <span>{{ props.row.project }}</span>
            </el-form-item>
            <el-form-item label="用例描述">
              <span>{{ props.row.description }}</span>
            </el-form-item>
          </el-form>
<!--          <el-collapse v-model="activeName" accordion>-->
<!--            <el-collapse-item name="1">-->
<!--              <template slot="title">-->
<!--                <span style="color: #99a9bf;">用例描述</span>-->
<!--                <i style="margin-left: 5px;" class="header-icon el-icon-info"></i>-->
<!--              </template>-->
<!--              <div>{{ props.row.description }}</div>-->
<!--            </el-collapse-item>-->
<!--          </el-collapse>-->
        </template>
      </el-table-column>
      <el-table-column
        label="Method"
        width="85px"
        prop="method"
        :filters="[{ text: 'get', value: 'get' }, { text: 'post', value: 'post' }, { text: 'put', value: 'put' }, { text: 'delete', value: 'delete' }]"
        :filter-method="filterHandler"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-tag v-if="scope.row.method==='post'" style="color: orangered;" type="warning">{{ scope.row.method }}</el-tag>
          <el-tag v-else-if="scope.row.method==='delete'" style="color: red;" type="danger">{{ scope.row.method }}</el-tag>
          <el-tag v-else-if="scope.row.method==='get'" style="color: #20b2aa;" type="success">{{ scope.row.method }}</el-tag>
          <el-tag v-else style="color: mediumblue;">{{ scope.row.method }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column show-overflow-tooltip label="Url" width="80px">
        <template slot-scope="scope">
          <span>{{ scope.row.url }}</span>
        </template>
      </el-table-column>
      <el-table-column show-overflow-tooltip label="Header" width="80px">
        <template slot-scope="scope">
          <span>{{ scope.row.header }}</span>
        </template>
      </el-table-column>
      <el-table-column show-overflow-tooltip label="Body" width="80px">
        <template slot-scope="scope">
          <span>{{ scope.row.body }}</span>
        </template>
      </el-table-column>
      <el-table-column show-overflow-tooltip align="center" label="Tag" width="100px">
        <template slot-scope="scope">
          <el-tag
            v-for="tag in handleTags(scope.row.tags)"
            :key="tag"
            size="mini"
            type="primary"
            effect="plain"
          >
            {{ tag }}
          </el-tag>
          <!--          <span>{{ scope.row.body }}</span>-->
        </template>
      </el-table-column>
      <el-table-column
        label="Status"
        width="85px"
        align="center"
        prop="status"
        :filters="[{ text: '正常', value: 1 }, { text: '禁用', value: 0 }]"
        :filter-method="filterHandler"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-tag v-if="scope.row.status" hit style="color: green;">正常</el-tag>
          <el-tag v-else type="info" hit>禁用</el-tag>
        </template>
      </el-table-column>
      <el-table-column v-if="showReviewer" label="创建者" width="110px" align="center">
        <template slot-scope="scope">
          <span style="color:red;">{{ scope.row.username }}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建日期" width="175px" align="center">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span style="margin-left: 5px">{{ formatDate(scope.row.created_at) }}</span>
        </template>
      </el-table-column>
      <!--      <el-table-column-->
      <!--        label="Mark"-->
      <!--        align="center"-->
      <!--        width="100px"-->
      <!--        prop="mark"-->
      <!--        :filters="[{ text: '高', value: 3 }, { text: '中', value: 2 }, { text: '低', value: 1 }]"-->
      <!--        :filter-method="filterHandler"-->
      <!--        filter-placement="bottom-end"-->
      <!--      >-->
      <!--        <template slot-scope="{row}">-->
      <!--          <el-rate v-model="row.imp" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" :max="3" style="margin-top:8px;" />-->
      <!--          &lt;!&ndash;          <svg-icon v-for="n in + row.imp" :key="n" icon-class="star" class="meta-item__icon" />&ndash;&gt;-->
      <!--        </template>-->
      <!--      </el-table-column>-->
      <el-table-column
        label="Imp"
        align="center"
        width="100px"
        prop="imp"
        :filters="[{ text: '高', value: 3 }, { text: '中', value: 2 }, { text: '低', value: 1 }]"
        :filter-method="filterHandler"
        filter-placement="bottom-end"
      >
        <template slot-scope="{row}">
          <el-rate v-model="row.imp" disabled :colors="['#99A9BF', '#f7c525', '#FF9900']" :max="4" style="margin-top:8px;" />
          <!--          <svg-icon v-for="n in + row.imp" :key="n" icon-class="star" class="meta-item__icon" />-->
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button v-if="row.status" size="mini" type="warning" @click="handleModifyStatus(row, 0)">
            禁用
          </el-button>
          <el-button v-else size="mini" type="success" @click="handleModifyStatus(row, 1)">
            启用
          </el-button>
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            编辑
          </el-button>
          <el-button size="mini" type="danger" @click="handleModifyStatus(row, 'delete')">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :per_page.sync="listQuery.per_page" @pagination="getList" />
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="100px" style="width: 400px; margin-left:50px;">
        <el-form-item label="用例名称" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="所属项目" prop="project">
          <el-input v-model="temp.project" />
        </el-form-item>
        <el-form-item label="用例描述" prop="description">
          <el-input v-model="temp.description" :autosize="{ minRows: 2, maxRows: 4}" type="textarea" placeholder="Please input" />
        </el-form-item>
        <el-form-item label="Method" prop="method">
          <el-select v-model="temp.method" class="filter-item" placeholder="Please select">
            <el-option v-for="item in methodTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item label="Url" prop="url">
          <el-input v-model="temp.url" />
        </el-form-item>
        <el-form-item label="Header" prop="header">
          <el-input v-model="temp.header" />
        </el-form-item>
        <el-form-item label="Body" prop="body">
          <el-input v-model="temp.body" />
        </el-form-item>
        <el-form-item label="Tag" prop="tags">
          <el-tag
            v-for="tag in dynamicTags"
            :key="tag"
            closable
            type="success"
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
          <el-button v-else plain type="primary" class="button-new-tag" size="small" @click="showInput">+ New Tag</el-button>
          <!--          <el-input v-model="temp.tag" />-->
        </el-form-item>
        <el-form-item label="Status">
          <el-select v-model="temp.status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in statusOptions" :key="item" :label="statusOptions[item]" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="Imp">
          <el-rate v-model="temp.imp" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" :max="3" style="margin-top:8px;" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

<!--    <el-dialog :visible.sync="dialogPvVisible" title="Reading statistics">-->
<!--      <el-table :data="pvData" border fit highlight-current-row style="width: 100%">-->
<!--        <el-table-column prop="key" label="Channel" />-->
<!--        <el-table-column prop="pv" label="Pv" />-->
<!--      </el-table>-->
<!--      <span slot="footer" class="dialog-footer">-->
<!--        <el-button type="primary" @click="dialogPvVisible = false">Confirm</el-button>-->
<!--      </span>-->
<!--    </el-dialog>-->
  </div>
</template>

<style>
  /*table expand begin*/
  .table-expand {
    font-size: 0;
  }
  .table-expand label {
    width: 90px;
    color: #99a9bf;
  }

  .table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
  /*table expand end*/
  /* tag begin*/
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
  /* tag end*/

</style>

<script>
import { getApiList, createApi, updateApi } from '@/api/apis'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
const methodTypeOptions = [
  { key: 'get', display_name: 'Get' },
  { key: 'post', display_name: 'Post' },
  { key: 'delete', display_name: 'Delete' },
  { key: 'put', display_name: 'Put' },
  { key: 'patch', display_name: 'Patch' }
]
// arr to obj, such as { CN : "China", US : "USA" }
const methodTypeKeyValue = methodTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})
export default {
  name: 'APisList',
  components: { Pagination },
  directives: { waves },
  filters: {
    // statusFilter(status) {
    //   const statusMap = {
    //     published: 'success',
    //     draft: 'info',
    //     deleted: 'danger'
    //   }
    //   return statusMap[status]
    // },
    typeFilter(type) {
      return methodTypeKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        per_page: 4,
        name: undefined,
        // type: undefined,
        sort: '+id'
      },
      methodTypeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['禁用', '启用'],
      showReviewer: false,
      // 自定义添加内容***begin******
      activeName: '1',
      multipleSelection: [],
      dynamicTags: [],
      inputVisible: false,
      inputValue: '',
      // *****end*****
      temp: {
        id: undefined,
        imp: '',
        tags: [],
        status: '启用',
        project: '',
        name: '',
        description: '',
        method: '',
        url: '',
        body: '',
        header: '',
        user_id: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      dialogPvVisible: false,
      rules: {
        method: [{ required: true, message: 'the method is required', trigger: 'blur' }],
        url: [{ required: true, message: 'the url is required', trigger: 'change' }],
        status: [{ required: true, message: 'the status is required', trigger: 'change' }],
        name: [{ required: true, message: 'the name is required', trigger: 'change' }],
        // timestamp: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        title: [{ required: true, message: 'title is required', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      getApiList(this.listQuery).then(response => {
        this.list = response.data.api_list
        this.total = response.data.total
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    // 自定义 ****begin****
    handleStatus(status) {
      if (Math.floor(status) === status) {
        return status ? '启用' : '禁用'
      } else {
        return status === '启用' ? 1 : 0
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    filterHandler(value, row, column) {
      const property = column['property']
      return row[property] === value
    },
    handleClose(tag) {
      this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1)
    },
    handleTags(tagStr) {
      if (tagStr === null) {
        return []
      }
      if (typeof (tagStr) === 'string') {
        return tagStr ? tagStr.split(',') : []
      } else {
        return tagStr ? tagStr.join(',') : ''
      }
    },
    formatDate(timeStr) {
      const date = new Date(timeStr)
      return date.toISOString().replace('T', ' ').replace('Z', '').split('.')[0]
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
        this.dynamicTags.push(inputValue)
      }
      this.inputVisible = false
      this.inputValue = ''
    },
    // ********end************
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleModifyStatus(row, status) {
      if (status === 'delete') {
        updateApi(row.id, { 'is_active': 0 }).then(() => {
          const index = this.list.indexOf(row)
          this.list.splice(index, 1)
          this.$message({
            message: 'delete Successfully',
            type: 'success'
          })
        })
      }
      updateApi(row.id, { 'status': status }).then(() => {
        this.$message({
          message: '操作Success',
          type: 'success'
        })
        row.status = status
      })
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.dynamicTags = []
      this.temp = {
        id: undefined,
        imp: 1,
        status: '启用',
        tags: [],
        project: '',
        name: '',
        description: '',
        method: '',
        url: '',
        body: '',
        header: '',
        user_id: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          this.temp.status = this.handleStatus(this.temp.status)
          this.temp.tags = this.handleTags(this.dynamicTags)
          this.temp.user_id = 3
          createApi(this.temp).then(() => {
            this.list.unshift(this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Created Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.dynamicTags = this.handleTags(this.temp.tags)
      this.temp.status = this.handleStatus(this.temp.status)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.tags = this.handleTags(this.dynamicTags)
          delete tempData['created_at']
          delete tempData['username']
          tempData.status = this.handleStatus(tempData.status)
          alert(JSON.stringify(tempData.status))
          updateApi(tempData.id, tempData).then(() => {
            this.temp.tags = this.handleTags(this.dynamicTags)
            this.temp.status = this.handleStatus(this.temp.status)
            for (const v of this.list) {
              if (v.id === this.temp.id) {
                const index = this.list.indexOf(v)
                this.list.splice(index, 1, this.temp)
                break
              }
            }
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDownload() {
      this.downloadLoading = true
        import('@/vendor/Export2Excel').then(excel => {
          const tHeader = ['ID', '用例名称', '所属项目', '用例描述', 'Method', 'Url', 'Body', '标志', '状态', '创建时间', '优先级', '操作者']
          const filterVal = ['id', 'name', 'project', 'description', 'method', 'url', 'body', 'tags', 'status', 'created_at', 'imp', 'username']
          const data = this.formatJson(filterVal, this.list)
          excel.export_json_to_excel({
            header: tHeader,
            data,
            filename: 'Apis'
          })
          this.downloadLoading = false
        })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}`
        ? 'ascending'
        : sort === `-${key}`
          ? 'descending'
          : ''
    }
  }
}
</script>
