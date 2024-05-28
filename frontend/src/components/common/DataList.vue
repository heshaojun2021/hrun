<template>
	<div class="data_box">
		<div class="title">{{ name }}</div>
		<el-scrollbar height="calc(100vh - 104px);">
			<el-menu default-active="1" class="el-menu-vertical-demo" active-text-color="#00aa7f" text-color="#000000" style="background: none;border: none;">
				<el-menu-item @click="selectEmit(item.id)" :index="item.id.toString()" v-for="item in datas" style="height: 35px;line-height: 35px;">
					<span :class="icon"></span>
					<span>{{ item.name }}</span>
				</el-menu-item>
				<el-menu-item @click="addEmit" style="height: 35px;line-height:35px;color: #00aaff;font-size: 14px;">
					<span class="el-icon-plus"></span>
					<span>添加</span>
				</el-menu-item>
			</el-menu>
		</el-scrollbar>
	</div>
</template>

<script>
export default {
	props: ['datas', 'name', 'icon','active'],
	emits: ['select', 'add'],
	methods: {
		selectEmit(index) {
			this.$emit('select', index);
		},
		addEmit() {
			this.$emit('add');
		}
	},
	computed:{
		activeItem(){
			if (this.active) return this.active.toString()
		}
	}
	
};
</script>

<style scoped>
.data_box {
	/* width: 180px; */
	box-shadow: 0 0 5px #00aa7f;
}
.title {
	text-align: center;
	font: bold 20px/40px 'microsoft yahei';
	border-bottom: solid 3px #878787;
}
</style>
